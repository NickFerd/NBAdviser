"""Helping classes and functions for adviser and strategies"""
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union

from nbadviser.config import ETC_TIMEZONE


def get_yesterday_est() -> str:
    """Convert naive local datetime to EST timezone and return date string
    in a form YYYY-MM-DD"""
    naive_now = datetime.datetime.now()
    est_now = naive_now.astimezone(ETC_TIMEZONE)
    est_yesterday = est_now - datetime.timedelta(days=1)
    return str(est_yesterday.date())


class GameBase(ABC):
    """Represents one game"""

    @property
    @abstractmethod
    def description(self):
        """Mandatory property"""
        raise NotImplementedError("You are calling Game base class")


@dataclass
class Recommendation:
    """Result of method execute() of any strategy"""
    title: str
    games: Union[List[GameBase], None]

    def to_html(self):
        """Format output as HTML"""
        template = f'\n<b><u>{self.title}</u></b>\n'

        if not self.games:
            template += 'В данной категории не нашлось игр\n'
            return template

        for game in self.games:
            template += f'{game.description}\n'

        return template

    def to_dict(self):
        pass

    def to_json(self):
        pass


class Recommendations:
    """Class holding all recommendations"""

    def __init__(self, recommendations: Optional[List[Recommendation]] = None):
        self.contents = recommendations or list()

    def append(self, item: Recommendation):
        self.contents.append(item)

    def to_html(self):
        template = f'<i>Игровой день: {get_yesterday_est()}</i>\n'
        if not self.contents:
            template += 'Не удалось найти интересные игры'
            return template

        for recommendation in self.contents:
            template += recommendation.to_html()

        return template


@dataclass
class Error:
    """Error holding class"""
    exception: Exception
    traceback: str
    label: str


# --------------- Strategies helpers ---------------

class Game(GameBase):
    def __init__(self, **kwargs):
        self.home_team_name = 'Undefined'
        self.home_team_score = float('nan')
        self.visitor_team_name = 'Undefined'
        self.visitor_team_score = float('nan')
        self.game_id: int = kwargs['GAME_ID']
        self.status: int = kwargs['GAME_STATUS_ID']
        self.home_team_id: int = kwargs['HOME_TEAM_ID']
        self.visitor_team_id: int = kwargs['VISITOR_TEAM_ID']

    def __repr__(self):
        return f'<Game>id={self.game_id}, game_status={self.status},' \
               f' home_team={self.home_team_name}, ' \
               f'home_team_score={self.home_team_score}, ' \
               f'visitor_team_name={self.visitor_team_name}, '\
               f'visitor_team_score={self.visitor_team_score}'

    def fill_score_and_team_name(self, **kwargs):
        team_id = kwargs['TEAM_ID']
        team_name = f'{kwargs["TEAM_CITY_NAME"]} {kwargs["TEAM_NAME"]}'
        team_score = kwargs['PTS']
        if team_id == self.home_team_id:
            self._fill_team_info('home', team_name, team_score)
        elif team_id == self.visitor_team_id:
            self._fill_team_info('visitor', team_name, team_score)

    def _fill_team_info(self, prefix: str, team_name: str, team_score: int):
        setattr(self, f'{prefix}_team_name', team_name)
        setattr(self, f'{prefix}_team_score', team_score)

    @property
    def score_gap(self):
        return abs(self.home_team_score - self.visitor_team_score)

    @property
    def description(self):
        return f'{self.visitor_team_name} - {self.home_team_name}'
