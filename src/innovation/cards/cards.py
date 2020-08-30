from __future__ import annotations
from src.innovation.utils.registry import Registerable
from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Deque, TYPE_CHECKING

if TYPE_CHECKING:
    from src.innovation.cards.card_effects import BaseEffect


@unique
class Color(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5


@unique
class SymbolType(Enum):
    LEAF = 1
    CROWN = 2
    LIGHT_BULB = 3
    CASTLE = 4
    FACTORY = 5
    CLOCK = 6


@unique
class Position(Enum):
    TOP_LEFT = 1
    BOTTOM_LEFT = 2
    BOTTOM_MIDDLE = 3
    BOTTOM_RIGHT = 4


@unique
class SplayDirection(Enum):
    NONE = 1
    LEFT = 2
    RIGHT = 3
    UP = 4


@dataclass
class Symbol:
    symbol_type: SymbolType
    position: Position


@dataclass(frozen=True)
class Card(Registerable):
    color: Color
    age: int
    symbols: List[Symbol]
    effects: List[BaseEffect]

    def __hash__(self):
        return super().__hash__()


@dataclass
class CardStack:
    stack: Deque[Card]
    splay: SplayDirection

    @property
    def is_empty(self):
        return not bool(self.stack)

    @property
    def top_card(self) -> Card:
        if not self.is_empty:
            return self.stack[-1]
