from src.innovation.cards.cards import Card, SymbolType, Color, SplayDirection
from src.innovation.cards.achievements import Achievement
from src.innovation.players.players import Player
from src.innovation.game.gamestate import GameState
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Set, Union, Callable
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


effect_building_blocks = Union[Primitive, SequenceOperator, Prompt, None]
game_state_to_card_set_func = Callable[
    [GameState, Player, Union[Player, None]], Set[Card]
]
card_set_to_effect_func = Callable[[Set[Card]], effect_building_blocks]


class BaseDogma(BaseEffect):
    @staticmethod
    @abstractmethod
    def dogma_effect(
        game_state: GameState, activating_player: Player
    ) -> effect_building_blocks:
        pass


class BaseDemand(BaseEffect):
    @staticmethod
    @abstractmethod
    def demand_effect(
        game_state: GameState, activating_player: Player, target_player: Player
    ) -> effect_building_blocks:
        pass

    @staticmethod
    def chained_dogma(
        game_state: GameState,
        activating_player: Player,
        demand_results: List[effect_building_blocks],
    ) -> effect_building_blocks:
        pass


@dataclass
class Optional(Prompt):
    operation: effect_building_blocks


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
    on_completion: card_set_to_effect_func = None
    reveal: bool = False


@dataclass
class Return(Prompt):
    allowed_cards: game_state_to_card_set_func
    min_cards: int
    max_cards: int
    on_completion: card_set_to_effect_func = None


@dataclass
class Meld(Primitive):
    allowed_cards: game_state_to_card_set_func
    min_cards: int = 1
    max_cards: Union[int] = 1
    on_completion: card_set_to_effect_func = None


@dataclass
class Achieve(Primitive):
    achievement: Achievement


@dataclass
class Tuck(Primitive):
    allowed_cards: game_state_to_card_set_func
    min_cards: int = 1
    max_cards: int = 1
    on_completion: card_set_to_effect_func = None


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
    allowed_cards: game_state_to_card_set_func
    card_location: CardLocation
    card_destination: CardLocation
    on_completion: card_set_to_effect_func = None
    num_cards: int = 1


@dataclass
class ExchangeCards(Primitive):
    allowed_giving_player: Set[Player]
    allowed_receiving_player: Set[Player]
    allowed_giving_cards: game_state_to_card_set_func
    allowed_receiving_cards: game_state_to_card_set_func
    num_cards_giving: int
    num_cards_receiving: int
    giving_location: CardLocation
    receiving_location: CardLocation
