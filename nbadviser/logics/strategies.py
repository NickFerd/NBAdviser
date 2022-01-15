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
    def execute(self, **kwargs) -> Recommendation:
        """Mandatory method that holds logic of choosing games and
        interaction with nba_api
        """
        raise NotImplementedError('You are calling method on ABC base class')


@register_strategy
class CloseGameStrategy(StrategyBase):
    """Chooses top X closest by score games from previous game day
    Score gap has to be equal or lower than min_gap attribute"""
    title = 'Напряженная концовка 🔥'

    game_id_index = 2
    finished_game_status = 3
    min_gap = 6  # Min value of score gap for game to be recommended
    top_games = 2  # Top 2 closest by score games

    def execute(self, **kwargs) -> Recommendation:
        """First, we create dict of games for that day and fill info about game
            and teams playing
        Second, fill scores for every game and team and calculate score gaps
        -----
        Optional keyword argument - games_date (str in format YYYY-MM-DD)
         to set specific date

        """
        specific_date = kwargs.get('games_date')
        if specific_date:
            game_date_str = specific_date
        else:
            game_date_str = get_yesterday_est()

        all_games = {}

        recommendation = Recommendation(title=self.title,
                                        games=None,
                                        )

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
        # collect score gaps from all finished games of the day
        for game in all_games.values():
            if game.status == self.finished_game_status:  # Only finished games
                gap = game.score_gap
                score_gaps[gap].append(game)

        # choose top games
        gaps = sorted(score_gaps.keys())[:self.top_games]
        close_games = []
        for gap in gaps:
            if gap >= self.min_gap:
                continue
            close_games.extend(score_gaps[gap])

        recommendation.games = close_games

        return recommendation

