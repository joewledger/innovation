from src.innovation.cards.card_registry import ConstructionDemand
from src.innovation.cards.cards import SymbolType
from src.innovation.cards.card_effects import Draw, TransferCard, CardLocation
import pytest
from mock import Mock


@pytest.mark.parametrize("hand_size", list(range(4)))
def test_construction_demand(hand_size):
    construction = ConstructionDemand()
    assert construction.symbol == SymbolType.CASTLE

    hand = {Mock() for _ in range(hand_size)}

    activating_player = Mock()
    target_player = Mock(hand=hand)

    def validate_draw(draw):
        assert isinstance(draw, Draw)
        assert draw.target_player == target_player
        assert draw.draw_location(Mock()) == CardLocation.HAND
        assert draw.level == 2

    effect = construction.demand_effect(Mock(), activating_player, target_player)
    if hand_size == 0:
        validate_draw(effect)
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.receiving_player == activating_player
        assert (
            effect.allowed_cards(Mock(), activating_player, target_player)
            == target_player.hand
        )
        assert effect.card_location == CardLocation.HAND
        assert effect.card_destination == CardLocation.HAND
        assert effect.num_cards == min(2, hand_size)
        validate_draw(effect.on_completion(Mock()))
