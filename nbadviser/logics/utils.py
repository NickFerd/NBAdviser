"""Helping classes and functions for adviser and strategies"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


class GameAbstract(ABC):
    """Represents one game"""

    @property
    @abstractmethod
    def description(self):
        """Mandatory property"""
        raise NotImplementedError("You are calling Game base class")


@dataclass
class Recommendation:
    """Strategy output"""
    title: str
    games: List[GameAbstract]

    def to_html(self):
        """Format output as HTML"""
        template = f'<b><u>{self.title}</u></b>\n'
        for game in self.games:
            template += f'\t{game.description}\n'

        return template

    def to_dict(self):
        pass

    def to_json(self):
        pass


class Recommendations:
    """Class holding all recommendations"""

    def __init__(self, recommendations: Optional[List[Recommendation]] = None):
        self._rc = recommendations or list()

    def append(self, item: Recommendation):
        self._rc.append(item)

    def to_html(self):
        template = ''
        for strategy_result in self._rc:
            template += strategy_result.to_html()

        return template


@dataclass
class Error:
    """Error holding class"""
    exception: Exception
    traceback: str

