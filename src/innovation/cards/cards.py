from src.innovation.utils.registry import ImmutableRegistry, Registerable
from src.innovation.cards.card_properties import Symbol, Color, SymbolType, Position, SplayDirection
from src.innovation.cards.card_effects import BaseDemand, BaseDogma
from dataclasses import dataclass
from typing import List, Union, Deque


@dataclass(frozen=True)
class Card(Registerable):
    color: Color
    age: int
    symbols: List[Symbol]
    effects: List[Union[BaseDogma, BaseDemand]]

    def __hash__(self):
        return super().__hash__()


@dataclass
class CardStack:
    stack: Deque[Card]
    splay: SplayDirection


GLOBAL_CARD_REGISTRY = ImmutableRegistry(
    [
        Card(
            name="Archery",
            color=Color.RED,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT)
            ],
            effects=[]
        ),
        Card(
            name="Sailing",
            color=Color.GREEN,
            age=1,
            symbols=[
                Symbol(SymbolType.CROWN, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT)
            ],
            effects=[]
        )
    ]
)


