"""File containing class for managing strategies
"""
import traceback

from nbadviser import strategies

from typing import Dict, List, Tuple

from nbadviser.logics.strategies import StrategyBase
from nbadviser.logics.utils import Error, Recommendations

Errors = List[Error]
Advise = Tuple[Recommendations, Errors]


class Adviser:
    """Class for managing strategies and producing output
    """
    def __init__(self, registered_strategies: Dict[str, StrategyBase]):
        self._strategies = registered_strategies

    def get_recommendations(self) -> Advise:
        """Execute all strategies

        Collect errors if strategy fails and continue with the next strategy.
        Done this way so that we could handle later this error but also execute
        rest of the strategies.
        """
        recommendations = Recommendations()
        errors = []
        for strategy in self._strategies.values():
            try:
                recommendation = strategy.execute()
                recommendations.append(recommendation)
            except Exception as err:
                errors.append(Error(exception=err,
                                    traceback=traceback.format_exc()))

        return recommendations, errors



adviser = Adviser(registered_strategies=strategies)
