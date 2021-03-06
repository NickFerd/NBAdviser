"""File containing class for managing strategies
"""
import traceback
from typing import Dict, List, Tuple, Optional, Any, Union

from nbadviser import strategies
from nbadviser.adviser.strategies import StrategyBaseABC, LiveGamesStrategy
from nbadviser.adviser.utils import Error, Recommendations, Recommendation

Errors = List[Error]
Advise = Tuple[Recommendations, Errors]


class Adviser:
    """Class for managing strategies

    Additional parameters that can be set using method - set_parameters:
    - games_date (string in a format YYYY-MM-DD)
    """

    def __init__(self, registered_strategies: Dict[str, StrategyBaseABC]):
        self._strategies = registered_strategies
        self._parameters = dict()

    def get_recommendations(self, **kwargs) -> Advise:
        """Execute all strategies

        Collect errors if strategy fails and continue with the next strategy.
        Done this way so that we could handle later this error but also execute
        rest of the strategies.
        Error handling happens on client side
        """
        recommendations = Recommendations(parameters=self._parameters)
        errors = []
        for strategy in self._strategies.values():
            try:
                recommendation = strategy.execute(**self._parameters)
                recommendations.append(recommendation)
            except Exception as err:
                errors.append(Error(exception=err,
                                    traceback=traceback.format_exc(),
                                    label=strategy.__class__.__name__))

        return recommendations, errors

    def get_live_games_or_none(self, **kwargs) -> Union[Recommendation, None]:
        """Get live games or None
        Exceptions are not forwarded to client"""
        try:
            strategy = LiveGamesStrategy()
            recommendation = strategy.execute(**self._parameters)
            if not recommendation.games:
                return
            return recommendation
        except Exception as err:
            return

    def set_parameters(self, **kwargs):
        """Set or update if already exists additional parameters that will
        be forwarded to Recommendations instance and
        every strategy when executing it"""
        if kwargs:
            for key, value in kwargs.items():
                self._parameters[key] = value

    def del_parameter(self, key) -> Optional[Any]:
        """Delete parameter
        :returns value if was set"""
        return self._parameters.pop(key, None)


adviser = Adviser(registered_strategies=strategies)
