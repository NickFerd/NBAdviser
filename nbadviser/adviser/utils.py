"""Helping classes and functions for adviser and strategies"""
import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum
from typing import List, Optional, Union, TypeVar

from nbadviser.config import ETC_TIMEZONE

# Create a generic variable that can be 'Parent', or any subclass.
AnyGame = TypeVar('AnyGame', bound='Game')


def get_date_etc_str() -> str:
    """Get EST timezone datetime and return date string in a form YYYY-MM-DD.
    Condition: if ETC time hour more or equal than 22 -> return current day
               else -> return previous day
    """
    timedelta_days = 1
    etc_now = datetime.datetime.now(tz=ETC_TIMEZONE)
    if etc_now.hour >= 22:
        timedelta_days = 0

    est_yesterday = etc_now - datetime.timedelta(days=timedelta_days)
    return str(est_yesterday.date())


@dataclass
class Team:
    """Class representing one team in a game"""
    team_id: int
    name: str = 'Undefined'
    score: Union[int, float] = float('nan')


@dataclass
class Teams:
    """Container for Team instances for easy access with dot notation"""
    home: Team
    visitor: Team

    def get_by_id(self, team_id: int):
        """Access team instance by the team_id"""
        for field in fields(self):
            team_instance = getattr(self, field.name)
            if team_instance.team_id == team_id:
                return team_instance


class GameABC(ABC):
    """Represents one game"""

    @property
    @abstractmethod
    def description(self):
        """Mandatory property"""
        raise NotImplementedError("You are calling Game base class")


class Game(GameABC):
    """Game object to use with data from ScoreboardV2 API endpoint
    but also possible to use with other"""

    def __init__(self, game_id: str, game_status: str,
                 game_status_id: int, teams: Teams = None,
                 **kwargs):
        self.game_id = game_id
        self.status = game_status
        self.status_id = game_status_id
        self.teams = teams

    def __repr__(self):
        return f'<Game>id={self.game_id}, game_status={self.status},' \
               f' home_team={self.teams.home.name},' \
               f' visitor_team = {self.teams.visitor.name}'

    @property
    def score_gap(self):
        return abs(self.teams.home.score - self.teams.visitor.score)

    @property
    def description(self):
        return f'{self.teams.visitor.name} - {self.teams.home.name}'


class GameStatus(Enum):
    LIVE = 2
    FINAL = 3


class GameWithTopPerformanceInfo(Game):
    """Game object with additional info about top performance of players"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_performers = []

    def fill_player_performance(self, **kwargs):
        player_name = kwargs.get('PTS_PLAYER_NAME')
        pts = kwargs.get('PTS')
        self.top_performers.append(f'{player_name} <b>{pts}</b> очк.')

    @property
    def description(self):
        return f'{", ".join(self.top_performers)} ' \
               f'(<i>{self.teams.visitor.name} - {self.teams.home.name}</i>)'


class GameWithScoreInfo(Game):
    """Game object with info of score in description"""

    @property
    def description(self):
        return f'{self.teams.visitor.name} - {self.teams.home.name} ' \
               f'({self.teams.visitor.score}-{self.teams.home.score}, ' \
               f'{self.status})'


@dataclass
class Recommendation:
    """Result of method execute() of any strategy"""
    title: str
    games: Union[List[GameABC], None] = None

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

    def __init__(self, recommendations: Optional[List[Recommendation]] = None,
                 parameters: Optional[dict] = None):
        self._contents = recommendations or list()
        self._parameters = parameters or dict()

    def append(self, item: Recommendation):
        self._contents.append(item)

    def to_html(self):
        specific_game_date = self._parameters.get('games_date')
        if specific_game_date:
            games_date = specific_game_date
        else:
            games_date = get_date_etc_str()

        template = f'<i>Игровой день: {games_date}</i>\n'
        if not self._contents:
            template += 'Не удалось найти интересные игры'
            return template

        for recommendation in self._contents:
            template += recommendation.to_html()

        return template


@dataclass
class Error:
    """Error holding class"""
    exception: Exception
    traceback: str
    label: str
