"""File containing strategies
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from functools import lru_cache
from typing import Callable, Any

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2
from nbadviser.logics.utils import Recommendation, Game, get_yesterday_est, \
    GameBase, GameWithTopPerformanceInfo

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

    @abstractmethod
    def get_raw_data_from_provider(self, **kwargs) -> Any:
        """Get raw data from nba_api or any provider"""
        raise NotImplementedError('You are calling method on ABC base class')

    @staticmethod
    def apply_parameters(**kwargs) -> dict:
        """Return dict of parameters to use in a strategy"""
        params = {}

        specific_date = kwargs.get('games_date')
        if specific_date:
            game_date_str = specific_date
        else:
            game_date_str = get_yesterday_est()

        params['games_date_str'] = game_date_str
        return params


class ScoreboardDataMixin(StrategyBase, ABC):
    """Class that implements getting raw data from ScoreboardV2
    nba_api endpoint and common processing.
    """

    @lru_cache(maxsize=5)
    def get_raw_data_from_provider(self, **kwargs) -> Any:
        """Get data from ScoreboardV2 endpoint"""

        game_date = kwargs.get('games_date_str')
        scoreboard = ScoreboardV2(game_date=game_date)

        return scoreboard

    @staticmethod
    def process_games_info(game_object: Callable, games_info: dict) -> dict:
        """Create dict of all games from raw data"""
        all_games = {}
        headers = games_info['headers']
        for one_game_info in games_info['data']:
            # feed Game instances with all data returned from NBA API
            one_game = game_object(**dict(zip(headers, one_game_info)))
            all_games[one_game.game_id] = one_game

        return all_games


@register_strategy
class CloseGameStrategy(ScoreboardDataMixin):
    """Chooses top X closest by score games from chosen game day
    Score gap has to be equal or lower than allowed_gap attribute"""
    title = 'Напряженная концовка 🔥'

    game_id_index = 2
    finished_game_status = 3
    allowed_gap = 6  # Min value of score gap for game to be recommended
    top_games = 2  # Top 2 closest by score games

    def execute(self, **kwargs) -> Recommendation:
        """First, we create dict of games for that day and fill info about game
            and teams playing
        Second, fill scores for every game and team and calculate score gaps
        -----
        Optional keyword argument - games_date (str in format YYYY-MM-DD)
         to set specific date

        """
        params = self.apply_parameters(**kwargs)

        recommendation = Recommendation(title=self.title,
                                        games=None)

        # Get raw information
        scoreboard = self.get_raw_data_from_provider(**params)
        # Info about games
        games_info = scoreboard.game_header.get_dict()
        all_games = self.process_games_info(Game, games_info)

        # Scores of every team that played
        teams_scores = scoreboard.line_score.get_dict()
        # Process teams scores
        headers = teams_scores['headers']
        for one_team_score in teams_scores['data']:
            game_id = one_team_score[self.game_id_index]
            game_inst = all_games[game_id]
            # provide all info from api
            game_inst.fill_score_and_team_name(**dict(zip(headers,
                                                          one_team_score)))

        # collect score gaps from all finished games of the day
        score_gaps = defaultdict(list)
        for game in all_games.values():
            if game.status == self.finished_game_status:  # Only finished games
                gap = game.score_gap
                score_gaps[gap].append(game)

        # choose top games
        gaps = sorted(score_gaps.keys())[:self.top_games]
        close_games = []
        for gap in gaps:
            if gap > self.allowed_gap:
                continue
            close_games.extend(score_gaps[gap])

        recommendation.games = close_games

        return recommendation


@register_strategy
class PerformanceStrategy(ScoreboardDataMixin):
    """Find games with impressive individual performance of any player
    Criteria: player scores more or equal than X points"""

    title = 'Индивидульные отжиги ⛹️'
    score_required = 37
    game_id_index = 2

    def execute(self, **kwargs) -> Recommendation:
        """Add info of top performance and then choose
        game with top individual scores"""
        params = self.apply_parameters(**kwargs)

        recommendation = Recommendation(title=self.title,
                                        games=None)

        games_with_top_performance = set()

        # Get raw information
        scoreboard = self.get_raw_data_from_provider(**params)
        # Info about games
        games_info = scoreboard.game_header.get_dict()
        all_games = self.process_games_info(GameWithTopPerformanceInfo,
                                            games_info)

        # Fill team names
        teams_scores = scoreboard.line_score.get_dict()
        headers = teams_scores['headers']
        for one_team_score in teams_scores['data']:
            game_id = one_team_score[self.game_id_index]
            game_inst = all_games[game_id]
            # provide all info from api
            game_inst.fill_score_and_team_name(**dict(zip(headers,
                                                          one_team_score)))

        # Team leaders
        team_leaders = scoreboard.team_leaders.get_dict()
        headers = team_leaders['headers']
        for top_performer in team_leaders['data']:
            top_performer_dict = dict(zip(headers, top_performer))
            if top_performer_dict['PTS'] >= self.score_required:
                game_instance = all_games.get(top_performer_dict['GAME_ID'])
                game_instance.fill_player_performance(**top_performer_dict)

                games_with_top_performance.add(game_instance)

        recommendation.games = list(games_with_top_performance)
        return recommendation
