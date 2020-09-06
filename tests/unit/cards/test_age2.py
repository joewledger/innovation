from src.innovation.cards.card_registry import ConstructionDemand, ConstructionDogma
from src.innovation.cards.cards import SymbolType, Color
from src.innovation.cards.card_effects import Achieve, Draw, TransferCard, CardLocation
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


@pytest.mark.parametrize(
    "colors, has_all_colors",
    [
        (set(), False),
        ({Color.RED}, False),
        ({Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE}, True),
    ],
)
def test_construction_dogma_has_all_colors(colors, has_all_colors):
    player = Mock(top_cards={Mock(color=color) for color in colors})

    assert ConstructionDogma.has_all_colors(player) == has_all_colors


@pytest.mark.parametrize(
    "activating_player_colors, other_player_colors, should_achieve",
    [
        (set(), set(), False),
        ({Color.RED}, {Color.YELLOW}, False),
        ({color for color in Color}, {color for color in Color}, False),
        ({color for color in Color}, {Color.RED}, True),
    ],
)
def test_construction_dogma(
    activating_player_colors, other_player_colors, should_achieve
):
    construction = ConstructionDogma()
    assert construction.symbol == SymbolType.CASTLE

    activating_player = Mock(
        top_cards={Mock(color=color) for color in activating_player_colors}
    )
    other_player = Mock(top_cards={Mock(color=color) for color in other_player_colors})
    game_state = Mock(players={activating_player, other_player})

    effect = construction.dogma_effect(game_state, activating_player)
    if not should_achieve:
        assert effect is None
    else:
        assert isinstance(effect, Achieve)
        assert effect.achievement.name == "Empire"
