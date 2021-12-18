"""File containing class for managing strategies
"""
from typing import Callable, Dict


class Handler:
    """Class for managing strategies
    """
    def __init__(self, strategies: Dict[str, Callable]):
        self._strategies = strategies

    def run(self):
        """Execute all strategies and make output"""
        print(self._strategies)
        for strategy in self._strategies.values():
            result = {}
            res = strategy.execute('2021-12-12')
            result[strategy.title] = res


