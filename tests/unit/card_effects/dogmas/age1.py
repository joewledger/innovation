from src.innovation.cards.card_registry import ArcheryDemand
from src.innovation.cards.cards import SymbolType
from src.innovation.cards.card_effects import Draw, CardLocation, TransferCard
from mock import Mock


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
