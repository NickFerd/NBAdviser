"""File containing strategies
"""

from abc import ABC, abstractmethod
from collections import defaultdict
from functools import lru_cache
from typing import Callable, Any, Dict, Type, Union

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

from nbadviser.adviser.utils import Recommendation, Game, get_yesterday_est, \
    GameWithTopPerformanceInfo, Team, Teams

# Easy initialization and registration of strategies
strategies = {}


def register_strategy(strategy_class: Callable):
    """Register and initialize a strategy"""
    strategies[strategy_class.__name__] = strategy_class()


class StrategyBaseABC(ABC):
    """Base class for strategy
    Strategies are used with register_strategy decorator,
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
    def get_raw_data(self, **kwargs) -> Any:
        """Get raw data from any provider"""
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


class ScoreboardDataMixin(StrategyBaseABC, ABC):
    """Class that implements getting raw data from ScoreboardV2
    nba_api endpoint and common preprocessing.
    """

    @staticmethod
    def get_raw_data(**kwargs) -> ScoreboardV2:
        """Get data from ScoreboardV2 endpoint"""
        game_date = kwargs.get('games_date_str')
        scoreboard = ScoreboardV2(game_date=game_date)
        return scoreboard

    def preprocess_data(self,
                        game_object: Type[Game], scoreboard: ScoreboardV2) \
            -> Dict[str, Union[Game, GameWithTopPerformanceInfo]]:
        """Create dict of all games instances for the day and fill with info
        of team names and scores"""

        all_games = self._collect_games(game_object=game_object,
                                        scoreboard=scoreboard)
        self._fill_name_and_score(all_games=all_games, scoreboard=scoreboard)

        return all_games

    @staticmethod
    def _collect_games(game_object: Type[Game],
                       scoreboard: ScoreboardV2) -> Dict[str, Game]:
        """"""
        all_games = {}
        _data = scoreboard.game_header.get_dict()
        headers = _data['headers']
        for game_data_list in _data['data']:
            game_data_dict = dict(zip(headers, game_data_list))
            game_id = game_data_dict['GAME_ID']
            game_status = game_data_dict['GAME_STATUS_TEXT']
            home_team = Team(team_id=game_data_dict['HOME_TEAM_ID'])
            visitor_team = Team(team_id=game_data_dict['VISITOR_TEAM_ID'])
            playing_teams = Teams(home=home_team, visitor=visitor_team)

            game = game_object(game_id=game_id, game_status=game_status,
                               teams=playing_teams)
            all_games[game.game_id] = game

        return all_games

    @staticmethod
    def _fill_name_and_score(all_games: Dict[str, Game],
                             scoreboard: ScoreboardV2) -> None:
        """Fill game instances with team names and scores"""
        team_scores = scoreboard.line_score.get_dict()
        headers = team_scores['headers']
        for one_team_score in team_scores['data']:
            score_dict = dict(zip(headers, one_team_score))
            game_id = score_dict['GAME_ID']
            team_name = f"{score_dict['TEAM_CITY_NAME']} " \
                        f"{score_dict['TEAM_NAME']}"
            team_id = score_dict['TEAM_ID']
            score = score_dict['PTS']

            game = all_games.get(game_id)
            team = game.teams.get_by_id(team_id=team_id)
            team.name = team_name
            team.score = score


@register_strategy
class CloseGameStrategy(ScoreboardDataMixin):
    """Chooses top X closest by score games from chosen game day
    Score gap has to be equal or lower than allowed_gap attribute"""
    title = 'Напряженная концовка 🔥'

    finished_game_status = 'Final'
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
        recommendation = Recommendation(title=self.title)

        # Get raw information and prepare raw data
        scoreboard = self.get_raw_data(**params)
        all_games = self.preprocess_data(Game, scoreboard)

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
class TopIndividualPerformanceStrategy(ScoreboardDataMixin):
    """Find games with impressive individual performance of any player
    Criteria: player scores more or equal than X points"""
    title = 'Индивидуальные отжиги ⛹️'

    score_required = 37

    def execute(self, **kwargs) -> Recommendation:
        """Add info of top performance and then choose
        game with top individual scores"""
        params = self.apply_parameters(**kwargs)

        recommendation = Recommendation(title=self.title,
                                        games=None)

        games_with_top_performance = set()

        # Get raw information and prepare raw_data
        scoreboard = self.get_raw_data(**params)
        all_games = self.preprocess_data(GameWithTopPerformanceInfo,
                                         scoreboard)

        # Team leaders
        team_leaders = scoreboard.team_leaders.get_dict()
        headers = team_leaders['headers']
        for top_performer in team_leaders['data']:
            top_performer_dict = dict(zip(headers, top_performer))
            if top_performer_dict['PTS'] >= self.score_required:
                game = all_games.get(top_performer_dict['GAME_ID'])
                game.fill_player_performance(**top_performer_dict)

                games_with_top_performance.add(game)

        recommendation.games = list(games_with_top_performance)
        return recommendation
