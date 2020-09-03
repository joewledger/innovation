from src.innovation.cards.card_registry import ArcheryDemand, CityStatesDemand
from src.innovation.cards.cards import SymbolType, CardStack, Color, Symbol, Position
from src.innovation.cards.card_effects import Draw, CardLocation, TransferCard
from src.innovation.players.players import Player
from mock import Mock
import pytest


def test_archery_demand():
    archery = ArcheryDemand()
    assert archery.symbol == SymbolType.CASTLE

    game_state = Mock()
    activating_player = Mock()
    target_player = Mock()
    target_player.hand = {Mock(age=1), Mock(age=2), Mock(age=3)}

    drawn_card = Mock(age=4)

    effect = archery.demand_effect(game_state, activating_player, target_player)
    assert isinstance(effect, Draw)

    assert effect.target_player == target_player
    assert effect.draw_location(drawn_card) == CardLocation.HAND
    assert effect.level == 1

    # Simulates what the draw does
    target_player.hand.add(drawn_card)

    on_completion_effect = effect.on_completion(drawn_card)
    assert isinstance(on_completion_effect, TransferCard)

    assert on_completion_effect.giving_player == target_player
    assert on_completion_effect.receiving_player == activating_player
    assert on_completion_effect.allowed_cards(
        game_state, activating_player, target_player
    ) == {drawn_card}

    assert on_completion_effect.card_location == CardLocation.HAND
    assert on_completion_effect.card_destination == CardLocation.HAND


@pytest.mark.parametrize(
    "target_player_symbol_count, target_player_top_cards, should_transfer",
    [
        ({}, set(), False),
        (
            {SymbolType.LEAF: 3, SymbolType.CASTLE: 3},
            {
                Mock(
                    symbols=[
                        Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
                    ]
                ),
                Mock(
                    symbols=[
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
                    ]
                ),
            },
            False,
        ),
        (
            {SymbolType.LEAF: 2, SymbolType.CASTLE: 4},
            {
                Mock(
                    symbols=[
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
                    ]
                ),
                Mock(
                    symbols=[
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
                    ]
                ),
            },
            True,
        ),
        (
            {SymbolType.LEAF: 5, SymbolType.CASTLE: 4, SymbolType.CROWN: 1},
            {
                Mock(
                    symbols=[
                        Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
                    ]
                ),
                Mock(
                    symbols=[
                        Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
                    ]
                ),
            },
            False,
        ),
    ],
)
def test_city_states_demand(
    target_player_symbol_count, target_player_top_cards, should_transfer
):
    city_states = CityStatesDemand()
    assert city_states.symbol == SymbolType.CROWN

    game_state = Mock()
    activating_player = Mock()
    target_player = Mock(
        symbol_count=target_player_symbol_count, top_cards=target_player_top_cards
    )

    effect = city_states.demand_effect(game_state, activating_player, target_player)
    if not should_transfer:
        assert effect is None
    else:
        transfered_card = Mock()
        drawn_card = Mock()

        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.receiving_player == activating_player
        assert effect.allowed_cards(game_state, activating_player, target_player) == {
            card
            for card in target_player_top_cards
            if any(symbol.symbol_type == SymbolType.CASTLE for symbol in card.symbols)
        }
        assert effect.card_location == CardLocation.BOARD
        assert effect.card_destination == CardLocation.BOARD

        on_completion_effect = effect.on_completion(transfered_card)
        assert isinstance(on_completion_effect, Draw)
        assert on_completion_effect.target_player == target_player
        assert on_completion_effect.draw_location(drawn_card) == CardLocation.HAND
        assert on_completion_effect.level == 1
