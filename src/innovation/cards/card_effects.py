from src.innovation.cards.cards import Card, SymbolType, Color, SplayDirection
from src.innovation.cards.achievements import Achievement
from src.innovation.players.players import Player
from src.innovation.game.gamestate import GameState
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, Union, Callable
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
    ) -> Union[Primitive, SequenceOperator, None]:
        pass


class BaseDemand(BaseEffect):
    @staticmethod
    @abstractmethod
    def demand_effect(
        game_state: GameState, activating_player: Player, target_player: Player
    ) -> Union[Primitive, SequenceOperator, None]:
        pass


@dataclass
class Optional(Prompt):
    operation: Union[Prompt, Primitive, SequenceOperator]


@unique
class CardLocation(Enum):
    HAND = 1
    BOARD = 2
    SCORE_PILE = 3
    DECK = 4


@dataclass
class Draw(Primitive):
    target_player: Player
    draw_location: Callable[[Set[Card]], CardLocation]
    repeat_effect: Callable[[Set[Card]], bool] = None
    level: int = None
    num_cards: int = 1
    on_completion: Callable[[Set[Card]], Union[Primitive, SequenceOperator, None]] = None
    reveal: bool = False


@dataclass
class Return(Prompt):
    allowed_cards: Callable[[GameState, Player, Player], Set[Card]]
    min_cards: int
    max_cards: int
    on_completion: Callable[[Set[Card]], Union[Primitive, SequenceOperator, None]] = None


@dataclass
class Meld(Primitive):
    allowed_cards: Callable[[GameState, Player, Player], Set[Card]]
    min_cards: int = 1
    max_cards: Union[int, None] = 1
    on_completion: Callable[[Set[Card]], Union[Primitive, SequenceOperator, None]] = None


@dataclass
class Achieve(Primitive):
    achievement: Achievement


@dataclass
class Tuck(Primitive):
    allowed_cards: Callable[[GameState, Player, Player], Set[Card]]
    min_cards: int = 1
    max_cards: int = 1
    on_completion: Callable[[Set[Card]], Union[Primitive, SequenceOperator, None]] = None


@dataclass
class Splay(Primitive):
    target_player: Player
    allowed_colors: Set[Color]
    allowed_directions: Set[SplayDirection]


@dataclass
class TransferCard(Primitive):
    giving_player: Player
    receiving_player: Player
    # function mapping (game_state, activating_player, target_player) -> set of cards that can be transferred
    allowed_cards: Callable[[GameState, Player, Player], Set[Card]]
    card_location: CardLocation
    card_destination: CardLocation
    on_completion: Callable[[Set[Card]], Union[Primitive, SequenceOperator, None]] = None
