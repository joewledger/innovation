from src.innovation.utils.registry import ImmutableRegistry
from src.innovation.cards.cards import Card, Color, Symbol, SymbolType, Position
from src.innovation.cards.card_effects import (
    And,
    BaseDemand,
    BaseDogma,
    Draw,
    DrawLocation,
    TransferCard,
)
from src.innovation.game.gamestate import GameState
from src.innovation.players.players import Player


class ArcheryDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def transfer_card_rule(_, __, target_player: Player):
        if len(target_player.hand) == 0:
            allowed_cards = set()
        else:
            max_age_in_target_hand = max(card.age for card in target_player.hand)
            allowed_cards = {
                card
                for card in target_player.hand
                if card.age == max_age_in_target_hand
            }

        return allowed_cards

    @staticmethod
    def demand_effect(
        game_state: GameState, activating_player: Player, target_player: Player
    ):
        return And(
            [
                Draw(
                    target_player=target_player,
                    draw_location=DrawLocation.HAND,
                    level=1,
                ),
                TransferCard(
                    giving_player=target_player,
                    receiving_player=activating_player,
                    allowed_cards=ArcheryDemand.transfer_card_rule,
                    card_location=target_player.hand,
                    card_destination=activating_player.hand,
                ),
            ]
        )


class SailingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        return Draw(
            target_player=activating_player, draw_location=DrawLocation.BOARD, level=1
        )


class WheelDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        return And(
            [
                Draw(activating_player, draw_location=DrawLocation.HAND, level=1),
                Draw(activating_player, draw_location=DrawLocation.HAND, level=1),
            ]
        )


GLOBAL_CARD_REGISTRY = ImmutableRegistry(
    [
        Card(
            name="Archery",
            color=Color.RED,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
            effects=[ArcheryDemand()],
        ),
        Card(
            name="Sailing",
            color=Color.GREEN,
            age=1,
            symbols=[
                Symbol(SymbolType.CROWN, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
            effects=[],
        ),
        Card(
            name="The Wheel",
            color=Color.GREEN,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
            effects=[],
        ),
    ]
)
