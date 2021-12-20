"""File containing class for managing strategies
"""
from nbadviser import strategies

from typing import Callable, Dict


class Adviser:
    """Class for managing strategies and producing output
    """
    def __init__(self, registered_strategies: Dict[str, Callable]):
        self._strategies = registered_strategies

    def get_recommendations(self):
        """Execute all strategies and make output"""
        print(self._strategies)
        result = {}
        for strategy in self._strategies.values():
            res = strategy.execute_strategy()
            result[strategy.__class__.__name__] = res

        return result


adviser = Adviser(registered_strategies=strategies)
