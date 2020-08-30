from src.innovation.cards.cards import Card, CardStack, SymbolType
from src.innovation.players.players import Player
from src.innovation.game.gamestate import GameState
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, Union, List, Callable
from enum import Enum, unique


class BaseEffect(ABC):
    @property
    @abstractmethod
    def symbol(self) -> SymbolType:
        pass


class Primitive:
    pass


class SequenceOperator:
    pass


class Prompt:
    pass


@dataclass
class ReturnUntilPass(Prompt):
    max_cards: int
    card_criteria: Callable[[Card], bool]
    post_effect: Callable[[Set[Card]], Union[Primitive, SequenceOperator]]


class BaseDogma(BaseEffect):
    @staticmethod
    @abstractmethod
    def dogma_effect(
        game_state: GameState, activating_player: Player
    ) -> Union[Primitive, SequenceOperator]:
        pass


class BaseDemand(BaseEffect):
    @staticmethod
    @abstractmethod
    def demand_effect(
        game_state: GameState, activating_player: Player, target_player: Player
    ) -> Union[Primitive, SequenceOperator]:
        pass


@dataclass
class And(SequenceOperator):
    members: List[Union[Primitive, SequenceOperator]]


@dataclass
class UpTo(SequenceOperator):
    primitive: Primitive
    num_times: int


@unique
class DrawLocation(Enum):
    HAND = 1
    BOARD = 2
    SCORE_PILE = 3


@dataclass
class Draw(Primitive):
    target_player: Player
    draw_location: DrawLocation
    level: int = None


@dataclass
class TransferCard(Primitive):
    giving_player: Player
    receiving_player: Player
    # function mapping (game_state, activating_player, target_player) -> set of cards that can be transferred
    allowed_cards: Callable[[GameState, Player, Player], Set[Card]]
    card_location: Union[Set[Card], CardStack]
    card_destination: Union[Set[Card], CardStack]
