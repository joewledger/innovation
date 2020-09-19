from src.innovation.utils.registry import (
    MutableRegistry,
    register_effect,
)
from src.innovation.cards.achievement_registry import GLOBAL_ACHIEVEMENTS_REGISTRY
from src.innovation.cards.cards import (
    Card,
    Color,
    Symbol,
    SymbolType,
    Position,
    SplayDirection,
    cards_with_symbol,
    get_highest_cards,
    get_lowest_cards,
)
from src.innovation.cards.card_effects import (
    BaseDemand,
    BaseDogma,
    Achieve,
    Draw,
    CardLocation,
    TransferCard,
    ExchangeCards,
    Meld,
    Return,
    Optional,
    Tuck,
    Splay,
    effect_building_blocks,
)
from src.innovation.game.gamestate import GameState
from src.innovation.players.players import Player
from typing import List, Set, Union


mutable_registry = MutableRegistry(
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
        ),
        Card(
            name="Metalworking",
            color=Color.RED,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Oars",
            color=Color.RED,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Agriculture",
            color=Color.YELLOW,
            age=1,
            symbols=[
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Domestication",
            color=Color.YELLOW,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Masonry",
            color=Color.YELLOW,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Clothing",
            color=Color.GREEN,
            age=1,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
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
        ),
        Card(
            name="Pottery",
            color=Color.BLUE,
            age=1,
            symbols=[
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Tools",
            color=Color.BLUE,
            age=1,
            symbols=[
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Writing",
            color=Color.BLUE,
            age=1,
            symbols=[
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CROWN, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Code of Laws",
            color=Color.PURPLE,
            age=1,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="City States",
            color=Color.PURPLE,
            age=1,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Mysticism",
            color=Color.PURPLE,
            age=1,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Construction",
            color=Color.RED,
            age=2,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Road Building",
            color=Color.RED,
            age=2,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Canal Building",
            color=Color.YELLOW,
            age=2,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CROWN, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Fermenting",
            color=Color.YELLOW,
            age=2,
            symbols=[
                Symbol(SymbolType.LEAF, Position.TOP_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Currency",
            color=Color.GREEN,
            age=2,
            symbols=[
                Symbol(SymbolType.LEAF, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Mapmaking",
            color=Color.GREEN,
            age=2,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Calendar",
            color=Color.BLUE,
            age=2,
            symbols=[
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Mathematics",
            color=Color.BLUE,
            age=2,
            symbols=[
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Monotheism",
            color=Color.PURPLE,
            age=2,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Philosophy",
            color=Color.PURPLE,
            age=2,
            symbols=[
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Engineering",
            color=Color.RED,
            age=3,
            symbols=[
                Symbol(SymbolType.CASTLE, Position.TOP_LEFT),
                Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Optics",
            color=Color.RED,
            age=3,
            symbols=[
                Symbol(SymbolType.CROWN, Position.TOP_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
            ],
        ),
        Card(
            name="Machinery",
            color=Color.YELLOW,
            age=3,
            symbols=[
                Symbol(SymbolType.LEAF, Position.TOP_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
            ],
        ),
        Card(
            name="Medicine",
            color=Color.YELLOW,
            age=3,
            symbols=[
                Symbol(SymbolType.CROWN, Position.TOP_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
            ],
        ),
        Card(
            name="Compass",
            color=Color.GREEN,
            age=3,
            symbols=[
                Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                Symbol(SymbolType.CROWN, Position.BOTTOM_MIDDLE),
                Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
            ],
        ),
    ]
)


@register_effect(registry=mutable_registry, card_name="Archery", position=0)
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
                allowed_receiving_players={activating_player},
                allowed_cards=ArcheryDemand.transfer_card_rule,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.HAND,
            ),
        )


@register_effect(registry=mutable_registry, card_name="Metalworking", position=0)
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


@register_effect(registry=mutable_registry, card_name="Oars", position=0)
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
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: transferable_cards,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.SCORE_PILE,
                on_completion=lambda _: Draw(
                    target_player=target_player,
                    draw_location=lambda _: CardLocation.HAND,
                    level=1,
                ),
            )

    @staticmethod
    def chained_dogma(
        game_state: GameState,
        activating_player: Player,
        demand_results: List[effect_building_blocks],
    ) -> effect_building_blocks:
        if all(result is None for result in demand_results):
            return Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.HAND,
                level=1,
            )


@register_effect(registry=mutable_registry, card_name="Agriculture", position=0)
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


@register_effect(registry=mutable_registry, card_name="Domestication", position=0)
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


@register_effect(registry=mutable_registry, card_name="Masonry", position=0)
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


@register_effect(registry=mutable_registry, card_name="Clothing", position=0)
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


@register_effect(registry=mutable_registry, card_name="Clothing", position=1)
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


@register_effect(registry=mutable_registry, card_name="Sailing", position=0)
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


@register_effect(registry=mutable_registry, card_name="The Wheel", position=0)
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


@register_effect(registry=mutable_registry, card_name="Pottery", position=0)
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


@register_effect(registry=mutable_registry, card_name="Pottery", position=1)
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


@register_effect(registry=mutable_registry, card_name="Tools", position=0)
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


@register_effect(registry=mutable_registry, card_name="Tools", position=1)
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


@register_effect(registry=mutable_registry, card_name="Writing", position=0)
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


@register_effect(registry=mutable_registry, card_name="Code of Laws", position=0)
class CodeOfLawsDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        colors_on_board = activating_player.colors_with_cards
        allowed_cards = {
            card for card in activating_player.hand if card.color in colors_on_board
        }

        if allowed_cards:
            return Optional(
                Tuck(
                    allowed_cards=lambda _, __, ___: allowed_cards,
                    on_completion=lambda cards: Optional(
                        Splay(
                            target_player=activating_player,
                            allowed_colors={card.color for card in cards},
                            allowed_directions={SplayDirection.LEFT},
                        )
                    ),
                )
            )


@register_effect(registry=mutable_registry, card_name="City States", position=0)
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
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: top_cards_with_castles,
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.BOARD,
                on_completion=lambda _: Draw(
                    target_player=target_player,
                    draw_location=lambda _: CardLocation.HAND,
                    level=1,
                ),
            )


@register_effect(registry=mutable_registry, card_name="Mysticism", position=0)
class MysticismDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
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


@register_effect(registry=mutable_registry, card_name="Construction", position=0)
class ConstructionDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, Draw]:
        draw = Draw(
            target_player=target_player,
            draw_location=lambda _: CardLocation.HAND,
            level=2,
        )

        if target_player.hand:
            return TransferCard(
                giving_player=target_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: target_player.hand,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.HAND,
                num_cards=min(2, len(target_player.hand)),
                on_completion=lambda _: draw,
            )
        else:
            return draw


@register_effect(registry=mutable_registry, card_name="Construction", position=1)
class ConstructionDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def has_all_colors(player: Player):
        all_colors = {color for color in Color}
        player_colors = {card.color for card in player.top_cards}
        return all_colors == player_colors

    @staticmethod
    def dogma_effect(
        game_state: GameState, activating_player: Player
    ) -> Union[Achieve, None]:
        if len(activating_player.top_cards) == 5 and not any(
            len(player.top_cards) == 5 and player != activating_player
            for player in game_state.players
        ):
            return Achieve(GLOBAL_ACHIEVEMENTS_REGISTRY.registry.get("Empire"))


@register_effect(registry=mutable_registry, card_name="Road Building", position=0)
class RoadBuildingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(
        game_state: GameState, activating_player: Player
    ) -> Union[Meld, None]:
        if activating_player.hand:
            return Meld(
                allowed_cards=lambda _, __, ___: activating_player.hand,
                min_cards=1,
                max_cards=2,
                on_completion=lambda cards: (
                    Optional(
                        ExchangeCards(
                            allowed_giving_player={activating_player},
                            allowed_receiving_player={
                                player
                                for player in game_state.players
                                if player != activating_player
                            },
                            allowed_giving_cards=lambda _, giving_player, __: {
                                giving_player.board.get(Color.RED).top_card
                            }
                            if Color.RED in giving_player.colors_with_cards
                            else {},
                            allowed_receiving_cards=lambda _, __, receiving_player: {
                                receiving_player.board.get(Color.GREEN).top_card
                            }
                            if Color.GREEN in receiving_player.colors_with_cards
                            else {},
                            num_cards_giving=1,
                            num_cards_receiving=1,
                            giving_location=CardLocation.BOARD,
                            receiving_location=CardLocation.BOARD,
                        )
                    )
                    if len(cards) == 2
                    else None
                ),
            )


@register_effect(registry=mutable_registry, card_name="Canal Building", position=0)
class CanalBuildingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if activating_player.hand or activating_player.score_pile:

            highest_cards_in_hand = get_highest_cards(activating_player.hand)
            highest_cards_in_score_pile = get_highest_cards(
                activating_player.score_pile
            )

            return Optional(
                ExchangeCards(
                    allowed_giving_player={activating_player},
                    allowed_receiving_player={activating_player},
                    allowed_giving_cards=lambda _, __, ___: highest_cards_in_hand,
                    allowed_receiving_cards=lambda _, __, ___: highest_cards_in_score_pile,
                    num_cards_giving=len(highest_cards_in_hand),
                    num_cards_receiving=len(highest_cards_in_score_pile),
                    giving_location=CardLocation.HAND,
                    receiving_location=CardLocation.SCORE_PILE,
                )
            )


@register_effect(registry=mutable_registry, card_name="Fermenting", position=0)
class FermentingDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Draw, None]:
        leaf_count = activating_player.symbol_count[SymbolType.LEAF]
        draw_count = leaf_count // 2

        if draw_count:
            return Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.HAND,
                level=2,
                num_cards=draw_count,
            )


@register_effect(registry=mutable_registry, card_name="Currency", position=0)
class CurrencyDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if activating_player.hand:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    min_cards=1,
                    max_cards=len(activating_player.hand),
                    on_completion=lambda cards: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.SCORE_PILE,
                        level=2,
                        num_cards=len({card.age for card in cards}),
                    ),
                )
            )


@register_effect(registry=mutable_registry, card_name="Mapmaking", position=0)
class MapmakingDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        target_cards = {card for card in target_player.score_pile if card.age == 1}

        if target_cards:
            return TransferCard(
                giving_player=target_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: target_cards,
                card_location=CardLocation.SCORE_PILE,
                card_destination=CardLocation.SCORE_PILE,
            )

    @staticmethod
    def chained_dogma(
        _,
        activating_player: Player,
        demand_results: List[effect_building_blocks],
    ) -> effect_building_blocks:
        if any(effect is not None for effect in demand_results):
            return Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.SCORE_PILE,
                level=1,
            )


@register_effect(registry=mutable_registry, card_name="Calendar", position=0)
class CalendarDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Draw, None]:
        if len(activating_player.score_pile) > len(activating_player.hand):
            return Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.HAND,
                level=3,
                num_cards=2,
            )


@register_effect(registry=mutable_registry, card_name="Mathematics", position=0)
class MathematicsDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if activating_player.hand:
            return Optional(
                Return(
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    min_cards=1,
                    max_cards=1,
                    on_completion=lambda cards: Draw(
                        target_player=activating_player,
                        draw_location=lambda _: CardLocation.BOARD,
                        level=list(cards)[0].age + 1,
                    ),
                )
            )


@register_effect(registry=mutable_registry, card_name="Monotheism", position=0)
class MonotheismDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        allowed_colors = (
            target_player.colors_with_cards - activating_player.colors_with_cards
        )

        if allowed_colors:
            return TransferCard(
                giving_player=target_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: {
                    card
                    for card in target_player.top_cards
                    if card.color in allowed_colors
                },
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.SCORE_PILE,
                on_completion=lambda _: Draw(
                    target_player=target_player,
                    draw_location=lambda _: CardLocation.BOARD,
                    level=1,
                    tuck=True,
                ),
            )


@register_effect(registry=mutable_registry, card_name="Monotheism", position=1)
class MonotheismDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Draw:
        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.BOARD,
            level=1,
            tuck=True,
        )


@register_effect(registry=mutable_registry, card_name="Philosophy", position=0)
class PhilosophyDogma1(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        splayable_colors = activating_player.splayable_colors
        if splayable_colors:
            return Optional(
                Splay(
                    target_player=activating_player,
                    allowed_colors=splayable_colors,
                    allowed_directions={SplayDirection.LEFT},
                )
            )


@register_effect(registry=mutable_registry, card_name="Philosophy", position=1)
class PhilosophyDogma2(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LIGHT_BULB

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if activating_player.hand:
            return Optional(
                TransferCard(
                    giving_player=activating_player,
                    allowed_receiving_players={activating_player},
                    allowed_cards=lambda _, __, ___: activating_player.hand,
                    card_location=CardLocation.HAND,
                    card_destination=CardLocation.SCORE_PILE,
                )
            )


@register_effect(registry=mutable_registry, card_name="Engineering", position=0)
class EngineeringDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        target_castle_cards = {
            card
            for card in target_player.top_cards
            if card.has_symbol_type(SymbolType.CASTLE)
        }
        if target_castle_cards:
            return TransferCard(
                giving_player=target_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: target_castle_cards,
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.SCORE_PILE,
                num_cards=len(target_castle_cards),
            )


@register_effect(registry=mutable_registry, card_name="Engineering", position=1)
class EngineeringDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CASTLE

    @staticmethod
    def dogma_effect(_, activating_player: Player) -> Union[Optional, None]:
        if Color.RED in activating_player.splayable_colors:
            return Optional(
                Splay(
                    target_player=activating_player,
                    allowed_colors={Color.RED},
                    allowed_directions={SplayDirection.LEFT},
                )
            )


@register_effect(registry=mutable_registry, card_name="Optics", position=0)
class OpticsDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def dogma_effect(game_state: GameState, activating_player: Player) -> Draw:
        players_with_less_points = {
            player
            for player in game_state.players
            if player.score < activating_player.score
        }
        transfer_card = (
            TransferCard(
                giving_player=activating_player,
                allowed_receiving_players=players_with_less_points,
                allowed_cards=lambda _, __, ___: activating_player.score_pile,
                card_location=CardLocation.SCORE_PILE,
                card_destination=CardLocation.SCORE_PILE,
            )
            if activating_player.score_pile and players_with_less_points
            else None
        )

        return Draw(
            target_player=activating_player,
            draw_location=lambda _: CardLocation.BOARD,
            level=3,
            on_completion=lambda cards: Draw(
                target_player=activating_player,
                draw_location=lambda _: CardLocation.SCORE_PILE,
                level=4,
            )
            if any(card.has_symbol_type(SymbolType.CROWN) for card in cards)
            else transfer_card,
        )


@register_effect(registry=mutable_registry, card_name="Machinery", position=0)
class MachineryDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[ExchangeCards, None]:
        highest_activating_player_cards = get_highest_cards(activating_player.hand)
        highest_target_player_cards = get_highest_cards(target_player.hand)

        if highest_activating_player_cards or highest_target_player_cards:
            return ExchangeCards(
                allowed_giving_player={activating_player},
                allowed_receiving_player={target_player},
                allowed_giving_cards=lambda _, __, ___: highest_activating_player_cards,
                allowed_receiving_cards=lambda _, __, ___: highest_target_player_cards,
                num_cards_giving=len(highest_activating_player_cards),
                num_cards_receiving=len(highest_target_player_cards),
                giving_location=CardLocation.HAND,
                receiving_location=CardLocation.HAND,
            )


@register_effect(registry=mutable_registry, card_name="Machinery", position=1)
class MachineryDogma(BaseDogma):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def dogma_effect(
        _, activating_player: Player
    ) -> Union[TransferCard, Optional, None]:
        cards_with_castles = {
            card
            for card in activating_player.hand
            if card.has_symbol_type(SymbolType.CASTLE)
        }

        splay = Optional(
            Splay(
                target_player=activating_player,
                allowed_colors={Color.RED},
                allowed_directions={SplayDirection.LEFT},
            )
        )

        if cards_with_castles:
            return TransferCard(
                giving_player=activating_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: cards_with_castles,
                card_location=CardLocation.HAND,
                card_destination=CardLocation.SCORE_PILE,
                on_completion=lambda _: splay,
            )
        elif Color.RED in activating_player.splayable_colors:
            return splay


@register_effect(registry=mutable_registry, card_name="Medicine", position=0)
class MedicineDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.LEAF

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[ExchangeCards, None]:
        if activating_player.score_pile or target_player.score_pile:
            lowest_activating_cards = get_lowest_cards(activating_player.score_pile)
            highest_target_cards = get_highest_cards(target_player.score_pile)

            return ExchangeCards(
                allowed_giving_player={activating_player},
                allowed_receiving_player={target_player},
                allowed_giving_cards=lambda _, __, ___: lowest_activating_cards,
                allowed_receiving_cards=lambda _, __, ___: highest_target_cards,
                num_cards_giving=min(1, len(activating_player.score_pile)),
                num_cards_receiving=min(1, len(target_player.score_pile)),
                giving_location=CardLocation.SCORE_PILE,
                receiving_location=CardLocation.SCORE_PILE,
            )


@register_effect(registry=mutable_registry, card_name="Compass", position=0)
class CompassDemand(BaseDemand):
    @property
    def symbol(self) -> SymbolType:
        return SymbolType.CROWN

    @staticmethod
    def cards_without_leaf(_, activating_player: Player, __) -> Set[Card]:
        return {
            card
            for card in activating_player.top_cards
            if not card.has_symbol_type(SymbolType.LEAF)
        }

    @staticmethod
    def demand_effect(
        _, activating_player: Player, target_player: Player
    ) -> Union[TransferCard, None]:
        target_transferable_cards = {
            card
            for card in target_player.top_cards
            if card.has_symbol_type(SymbolType.LEAF) and card.color != Color.GREEN
        }
        activating_transferable_cards = {
            card
            for card in activating_player.top_cards
            if not card.has_symbol_type(SymbolType.LEAF)
        }

        if target_transferable_cards:
            return TransferCard(
                giving_player=target_player,
                allowed_receiving_players={activating_player},
                allowed_cards=lambda _, __, ___: target_transferable_cards,
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.BOARD,
                on_completion=lambda _: TransferCard(
                    giving_player=activating_player,
                    allowed_receiving_players={target_player},
                    allowed_cards=CompassDemand.cards_without_leaf,
                    card_location=CardLocation.BOARD,
                    card_destination=CardLocation.BOARD,
                ),
            )
        elif activating_transferable_cards:
            return TransferCard(
                giving_player=activating_player,
                allowed_receiving_players={target_player},
                allowed_cards=lambda _, __, ___: activating_transferable_cards,
                card_location=CardLocation.BOARD,
                card_destination=CardLocation.BOARD,
            )


GLOBAL_CARD_REGISTRY = mutable_registry.to_immutable_registry()
