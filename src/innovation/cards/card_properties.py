from enum import Enum, unique
from dataclasses import dataclass


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
