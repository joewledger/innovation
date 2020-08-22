from src.innovation.card_properties import Symbol, Color, SymbolType, Position
from src.innovation.card_effects import BaseDemand, BaseDogma
from dataclasses import dataclass
from frozendict import frozendict
from typing import List, Union


@dataclass(frozen=True)
class Card:
    name: str
    color: Color
    age: int
    symbols: List[Symbol]
    effects: List[Union[BaseDogma, BaseDemand]]


class ImmutableCardRegistry:
    def __init__(self, cards: List[Card]):
        self._cards = frozendict({card.name: card for card in cards})

    @property
    def cards(self) -> frozendict:
        return self._cards


GLOBAL_CARD_REGISTRY = ImmutableCardRegistry(
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
