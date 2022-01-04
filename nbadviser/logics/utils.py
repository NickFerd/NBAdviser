"""Helping classes and functions for adviser and strategies"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


class GameBase(ABC):
    """Represents one game"""

    @property
    @abstractmethod
    def description(self):
        """Mandatory property"""
        raise NotImplementedError("You are calling Game base class")


@dataclass
class Recommendation:
    """Result of method execute() of any strategy"""
    title: str
    games: List[GameBase]

    def to_html(self):
        """Format output as HTML"""
        template = f'<b><u>{self.title}</u></b>\n'
        for game in self.games:
            template += f'\t\t{game.description}\n'

        return template

    def to_dict(self):
        pass

    def to_json(self):
        pass


class Recommendations:
    """Class holding all recommendations"""

    def __init__(self, recommendations: Optional[List[Recommendation]] = None):
        self.contents = recommendations or list()

    def append(self, item: Recommendation):
        self.contents.append(item)

    def to_html(self):
        if not self.contents:
            return 'Не удалось подобрать игры'

        template = ''
        for recommendation in self.contents:
            template += recommendation.to_html()

        return template


@dataclass
class Error:
    """Error holding class"""
    exception: Exception
    traceback: str
    label: str

