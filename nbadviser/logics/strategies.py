"""File containing strategies
"""
from abc import ABC, abstractmethod
from typing import List, Callable


# Easy initialization and registration of new strategies
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
    def execute(self, game_day: str):
        """Mandatory method that holds logic of choosing games and
        interaction with nba_api
        """
        raise NotImplementedError('You are calling method on ABC base class')


@register_strategy
class CloseGameStrategy(StrategyBase):
    """Chooses closest by score games"""
    title = 'Самая близкая по счету'

    def execute(self, game_day: str) -> List[str]:
        """Chooses closest game for given day
        """
        print('Hello')
        print(self.title)
        return ['bak', 'boo']
