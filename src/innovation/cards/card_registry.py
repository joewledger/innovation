from src.innovation.utils.registry import ImmutableRegistry
from src.innovation.cards.achievement_registry import GLOBAL_ACHIEVEMENTS_REGISTRY
from src.innovation.cards.cards import (
    Card,
    Color,
    Symbol,
    SymbolType,
    Position,
    SplayDirection,
    cards_with_symbol,
)
from src.innovation.cards.card_effects import (
    BaseDemand,
    BaseDogma,
    Achieve,
    Draw,
    CardLocation,
    TransferCard,
    Meld,
    Return,
    Optional,
    Tuck,
    Splay,
)
from src.innovation.game.gamestate import GameState
from src.innovation.players.players import Player
from typing import Set, Union


class ArcheryDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def transfer_card_rule(_, __, target_player: Player) -> Set[Card]:
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
    ) -> Draw:
        return Draw(
            target_player=target_player,
            draw_location=lambda _: CardLocation.HAND,
            level=1,
            on_completion=lambda _: TransferCard(
                giving_player=target_player,
                receiving_player=activating_player,
                allowed_cards=ArcheryDemand.transfer_card_rule,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.HAND,
            ),
        )


class MetalWorkingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def has_castle(cards: Set[Card]) -> bool:
        return len(cards_with_symbol(cards, SymbolType.CASTLE)) > 0

    @staticmethod
    def draw_location(cards: Set[Card]) -> CardLocation:
        if MetalWorkingDogma.has_castle(cards):
            return CardLocation.SCORE_PILE
        else:
            return CardLocation.HAND

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
        return Draw(
            target_player=activating_player,
            draw_location=MetalWorkingDogma.draw_location,
            repeat_effect=MetalWorkingDogma.has_castle,
            level=1,
            reveal=True,
        )


class OarsDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def demand_effect(
        game_state: GameState, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        transferable_cards = cards_with_symbol(target_player.hand, SymbolType.CROWN)

        if transferable_cards:
            return TransferCard(
                giving_player=target_player,
                receiving_player=activating_player,
                allowed_cards=lambda _, __, ___: transferable_cards,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.SCORE_PILE,
                on_completion=lambda _: Draw(
                    target_player=target_player,
                    draw_location=lambda _: CardLocation.HAND,
                    level=1,
                ),
            )


class AgricultureDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if len(activating_player.hand) >= 1:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    min_cards=1,
                    max_cards=1,
                    on_completion=lambda cards: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.SCORE_PILE,
                        level=list(cards)[0].age + 1,
                    ),
                )
            )


class DomesticationDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def allowed_cards(_, activating_player: Player, __) -> Set[Card]:
        if not activating_player.hand:
            return set()

        min_age = min(card.age for card in activating_player.hand)
        return {card for card in activating_player.hand if card.age == min_age}

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Draw, Meld]:
        draw = Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.HAND,
            level=1,
        )

        if not activating_player.hand:
            return draw
        else:
            return Meld(
                allowed_cards=DomesticationDogma.allowed_cards,
                on_completion=lambda _: draw,
            )


class MasonryDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def on_completion(cards: Set[Card]) -> Union[Achieve, None]:
        if len(cards) >= 4:
            return Achieve(GLOBAL_ACHIEVEMENTS_REGISTRY.registry.get("Monument"))

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        meldable_cards = cards_with_symbol(activating_player.hand, SymbolType.CASTLE)
        if meldable_cards:
            return Optional(
                Meld(
                    min_cards=1,
                    max_cards=len(meldable_cards),
                    allowed_cards=lambda _, __, ___: meldable_cards,
                    on_completion=MasonryDogma.on_completion,
                )
            )


class ClothingDogma1(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Meld, None]:
        colors_with_cards = activating_player.colors_with_cards
        allowed_cards = {
            card
            for card in activating_player.hand
            if card.color not in colors_with_cards
        }

        if allowed_cards:
            return Meld(allowed_cards=lambda _, __, ___: allowed_cards)


class ClothingDogma2(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(
        game_state: GameState, activating_player: Player
    ) -> Union[Draw, None]:
        colors_on_board = activating_player.colors_with_cards
        colors_on_other_boards = set().union(
            *[
                player.colors_with_cards
                for player in game_state.players
                if player != activating_player
            ]
        )

        num_unique_colors = len(colors_on_board - colors_on_other_boards)

        if num_unique_colors > 0:
            return Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.SCORE_PILE,
                level=1,
                num_cards=num_unique_colors,
            )


class SailingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.BOARD,
            level=1,
        )


class WheelDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.HAND,
            level=1,
            on_completion=lambda _: Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.HAND,
                level=1,
            ),
        )


class PotteryDogma1(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if activating_player.hand:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    min_cards=1,
                    max_cards=3,
                    on_completion=lambda cards: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.SCORE_PILE,
                        level=len(cards),
                    ),
                )
            )


class PotteryDogma2(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.HAND,
            level=1,
        )


class ToolsDogma1(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if len(activating_player.hand) >= 3:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    min_cards=3,
                    max_cards=3,
                    on_completion=lambda _: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.BOARD,
                        level=3,
                    ),
                )
            )


class ToolsDogma2(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        age_3_cards = {card for card in activating_player.hand if card.age == 3}

        if age_3_cards:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: age_3_cards,
                    min_cards=1,
                    max_cards=1,
                    on_completion=lambda _: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.HAND,
                        level=1,
                        num_cards=3,
                    ),
                )
            )


class WritingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.HAND,
            level=2,
        )


class CodeOfLawsDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        colors_on_board = activating_player.colors_with_cards
        allowed_cards = {
            card for card in activating_player.hand if card.color in colors_on_board
        }

        return Optional(
            Tuck(
                allowed_cards=lambda _: allowed_cards,
                on_completion=lambda cards: Optional(
                    Splay(
                        target_player=activating_player,
                        allowed_colors={card.color for card in cards},
                        allowed_directions={SplayDirection.LEFT},
                    )
                ),
            )
        )


class CityStatesDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        top_cards_with_castles = {
            card
            for card in target_player.top_cards
            if any(symbol.symbol_type == SymbolType.CASTLE for symbol in card.symbols)
        }

        if (
            target_player.symbol_count.get(SymbolType.CASTLE, 0) >= 4
            and top_cards_with_castles
        ):
            return TransferCard(
                giving_player=target_player,
                receiving_player=activating_player,
                allowed_cards=lambda _, __, ___: top_cards_with_castles,
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.BOARD,
                on_completion=lambda _: Draw(
                    target_player=target_player,
                    draw_location=lambda _: CardLocation.HAND,
                    level=1,
                ),
            )


class MysticismDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player):
        colors_on_board = activating_player.colors_with_cards

        return Draw(
            target_player=activating_player,
            draw_location=lambda cards: CardLocation.BOARD
            if any(card.color in colors_on_board for card in cards)
            else CardLocation.HAND,
            level=1,
            on_completion=lambda cards: Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.HAND,
                level=1,
            )
            if any(card.color in colors_on_board for card in cards)
            else None,
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
