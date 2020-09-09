from __future__ import annotations
from src.innovation.utils.registry import Registerable
from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Deque, Dict, Set, TYPE_CHECKING

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


@dataclass
class Card(Registerable):
    color: Color
    age: int
    symbols: List[Symbol]
    effects: List[BaseEffect] = None

    def __eq__(self, other):
        return super().__eq__(other)

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

    @property
    def can_splay(self) -> bool:
        return len(self.stack) >= 2

    @property
    def symbol_count(self) -> Dict[SymbolType, int]:
        symbols_to_count = []

        # Mapping of splay direction to set of symbol positions which should be counted
        symbol_count_rules = {
            SplayDirection.NONE: set(),
            SplayDirection.LEFT: {Position.BOTTOM_RIGHT},
            SplayDirection.RIGHT: {Position.TOP_LEFT, Position.BOTTOM_LEFT},
            SplayDirection.UP: {
                Position.BOTTOM_LEFT,
                Position.BOTTOM_MIDDLE,
                Position.BOTTOM_RIGHT,
            },
        }

        if not self.is_empty:
            symbols_to_count.extend(self.top_card.symbols)

        for card in list(self.stack)[:-1]:
            symbols_to_count.extend(
                [
                    symbol
                    for symbol in card.symbols
                    if symbol.position in symbol_count_rules.get(self.splay, set())
                ]
            )

        return {
            symbol_type: sum(
                1 for symbol in symbols_to_count if symbol.symbol_type == symbol_type
            )
            for symbol_type in SymbolType
        }


def cards_with_symbol(cards: Set[Card], symbol: SymbolType) -> Set[Card]:
    return {card for card in cards if symbol in (s.symbol_type for s in card.symbols)}
