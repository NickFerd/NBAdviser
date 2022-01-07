"""File containing strategies
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Callable

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nbadviser.logics.utils import Recommendation, Game, get_yesterday_est

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
    """Chooses top 2 closest by score games from previous game day"""
    title = 'Напряженная концовка 🔥'

    game_id_index = 2
    finished_game_status = 3
    min_gap = 6  # Min value of score gap for game to be recommended

    def execute(self) -> Recommendation:
        """Chooses closest game for the previous game day
        First, we create dict of games for that day and fill info about game
            and teams playing
        Second, fill scores for every game and team and calculate score gaps
        """
        game_date_str = get_yesterday_est()
        all_games = {}

        # Get raw information from nba_api
        scoreboard_for_yesterday = ScoreboardV2(game_date=game_date_str)
        # Info about games
        games_info = scoreboard_for_yesterday.game_header.get_dict()
        # Scores of every team that played
        teams_scores = scoreboard_for_yesterday.line_score.get_dict()

        # Process game info
        headers = games_info['headers']
        for one_game_info in games_info['data']:
            # feed Game instances with all data returned from NBA API
            one_game = Game(**dict(zip(headers, one_game_info)))
            all_games[one_game.game_id] = one_game

        # Process teams scores
        headers = teams_scores['headers']
        for one_team_score in teams_scores['data']:
            game_id = one_team_score[self.game_id_index]
            game_inst = all_games[game_id]
            # provide all info from api
            game_inst.fill_score_and_team_name(**dict(zip(headers,
                                                          one_team_score)))
        score_gaps = defaultdict(list)
        # determine closest game/games
        for game in all_games.values():
            if game.status == self.finished_game_status:  # Only finished games
                gap = game.score_gap
                score_gaps[gap].append(game)

        min_gap = min(score_gaps.keys())

        # Only really close games
        if min_gap > self.min_gap:
            return Recommendation(title=self.title,
                                  games=None)

        closest_games = score_gaps[min_gap]
        score_gaps.pop(min_gap)

        # ---------
        min_gap = min(score_gaps.keys())
        if min_gap <= self.min_gap:
            closest_games.extend(score_gaps[min_gap])
            score_gaps.pop(min_gap)

        recommendation = Recommendation(title=self.title,
                                        games=closest_games)
        return recommendation

