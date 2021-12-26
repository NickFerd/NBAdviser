"""File containing strategies
"""
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nbadviser.logics.utils import Recommendation, GameAbstract

# Easy initialization and registration of strategies
strategies = {}


def register_strategy(strategy_class: Callable):
    """Register and initialize a strategy"""
    strategies[strategy_class.__name__] = strategy_class()


class StrategyBase(ABC):
    """Base class for strategy
    Only used with register_strategy decorator,
    not intended to be called directly
    """

    @property
    @abstractmethod
    def title(self) -> str:
        """Mandatory property which define title of strategy
        """
        raise NotImplementedError('You are calling method on ABC base class')

    @abstractmethod
    def execute(self) -> Recommendation:
        """Mandatory method that holds logic of choosing games and
        interaction with nba_api
        """
        raise NotImplementedError('You are calling method on ABC base class')


@register_strategy
class CloseGameStrategy(StrategyBase):
    """Chooses top closest by score games from previous game day"""
    title = 'Близкие по счету игры'
    days_offset = -1  # Previous game day
    game_id_index = 2

    def execute(self) -> Recommendation:
        """Chooses closest game for the previous game day
        First, we create dict of games for that day and fill info about game
            and teams playing
        Second, fill scores for every game and team and calculate score gaps
        """
        games = {}

        # Get raw information from nba_api
        scoreboard_for_yesterday = ScoreboardV2(day_offset=self.days_offset)
        # Info about games
        games_info = scoreboard_for_yesterday.game_header.get_dict()
        # Scores of every team that played
        teams_scores = scoreboard_for_yesterday.line_score.get_dict()

        # Process game info
        headers = games_info['headers']
        for one_game_info in games_info['data']:
            # feed Game instances with all data returned from NBA API
            game = Game(**dict(zip(headers, one_game_info)))
            games[game.game_id] = game

        # Process teams scores
        headers = teams_scores['headers']
        for one_team_score in teams_scores['data']:
            game_id = one_team_score[self.game_id_index]
            game_inst = games[game_id]
            # provide all info from api
            game_inst.fill_score_and_team_name(**dict(zip(headers,
                                                          one_team_score)))
        score_gaps = defaultdict(list)
        # determine closest game/games
        for game in games.values():
            if game.status == 3:  # Only finished games
                gap = game.score_gap
                score_gaps[gap].append(game)

        min_gap = min(score_gaps.keys())
        games = score_gaps[min_gap]
        recommendation = Recommendation(title=self.title,
                                        games=games)
        print(recommendation)
        return recommendation


class Game(GameAbstract):
    def __init__(self, **kwargs):
        self.home_team_name = 'Undefined'
        self.home_team_score = float('nan')
        self.visitor_team_name = 'Undefined'
        self.visitor_team_score = float('nan')
        try:
            self.game_id: int = kwargs['GAME_ID']
            self.status: int = kwargs['GAME_STATUS_ID']
            self.home_team_id: int = kwargs['HOME_TEAM_ID']
            self.visitor_team_id: int = kwargs['VISITOR_TEAM_ID']
        except KeyError:
            raise  # todo add custom exception ApiError

    def __repr__(self):
        return f'<Game>id={self.game_id}, game_status={self.status},' \
               f' home_team={self.home_team_name}, ' \
               f'home_team_score={self.home_team_score}, ' \
               f'visitor_team_name={self.visitor_team_name}, '\
               f'visitor_team_score={self.visitor_team_score}'

    def fill_score_and_team_name(self, **kwargs):
        try:
            team_id = kwargs['TEAM_ID']
            team_name = f'{kwargs["TEAM_CITY_NAME"]} {kwargs["TEAM_NAME"]}'
            team_score = kwargs['PTS']
            if team_id == self.home_team_id:
                self._fill_team_info('home', team_name, team_score)
            elif team_id == self.visitor_team_id:
                self._fill_team_info('visitor', team_name, team_score)
            else:
                pass  # todo add custom error for unconsinstent data
        except KeyError:
            raise  # todo add custom Api error

    def _fill_team_info(self, prefix: str, team_name: str, team_score: int):
        setattr(self, f'{prefix}_team_name', team_name)
        setattr(self, f'{prefix}_team_score', team_score)

    @property
    def score_gap(self):
        return abs(self.home_team_score - self.visitor_team_score)

    @property
    def description(self):
        return f'{self.home_team_name} - {self.visitor_team_name}, ' \
               f'Разница в счете {self.score_gap}'


# @register_strategy
# class NewStrategy(StrategyBase):
#     title = 'New fancy strategy'
#
#     def execute(self):
#         raise RuntimeError('testing error handling')
