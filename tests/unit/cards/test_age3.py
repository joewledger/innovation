from src.innovation.cards.card_registry import EngineeringDemand, EngineeringDogma
from src.innovation.cards.cards import SymbolType, Color, SplayDirection
from src.innovation.cards.card_effects import (
    Optional,
    Splay,
    TransferCard,
    CardLocation,
)
import pytest
from mock import Mock


@pytest.mark.parametrize(
    "top_cards",
    [
        set(),
        {Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CASTLE)},
        {Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CASTLE)},
    ],
)
def test_engineering_demand(top_cards):
    engineering = EngineeringDemand()
    assert engineering.symbol == SymbolType.CASTLE

    activating_player = Mock()
    target_player = Mock(top_cards=top_cards)

    transfer_cards = {
        card for card in top_cards if card.has_symbol_type(SymbolType.CASTLE)
    }
    effect = engineering.demand_effect(Mock(), activating_player, target_player)

    if not transfer_cards:
        assert effect is None
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.allowed_receiving_players == {activating_player}
        assert (
            effect.allowed_cards(Mock(), activating_player, target_player)
            == transfer_cards
        )
        assert effect.card_location == CardLocation.BOARD
        assert effect.card_destination == CardLocation.SCORE_PILE
        assert effect.num_cards == len(transfer_cards)


@pytest.mark.parametrize(
    "splayable_colors, should_splay",
    [
        (set(), False),
        ({Color.RED}, True),
        ({Color.YELLOW}, False),
        ({Color.RED, Color.YELLOW}, True),
    ],
)
def test_engineering_dogma(splayable_colors, should_splay):
    engineering = EngineeringDogma()
    assert engineering.symbol == SymbolType.CASTLE

    activating_player = Mock(splayable_colors=splayable_colors)

    effect = engineering.dogma_effect(Mock(), activating_player)
    if not should_splay:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Splay)
        assert operation.target_player == activating_player
        assert operation.allowed_colors == {Color.RED}
        assert operation.allowed_directions == {SplayDirection.LEFT}
