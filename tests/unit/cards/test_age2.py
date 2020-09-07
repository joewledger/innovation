from src.innovation.cards.card_registry import (
    ConstructionDemand,
    ConstructionDogma,
    RoadBuildingDogma,
)
from src.innovation.cards.cards import SymbolType, Color
from src.innovation.cards.card_effects import (
    Achieve,
    Draw,
    TransferCard,
    CardLocation,
    Meld,
    Optional,
    ExchangeCards,
)
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


@pytest.mark.parametrize(
    "activating_hand, receiving_colors_on_board",
    [
        (set(), set()),
        ({Mock()}, {Color.GREEN}),
        ({Mock(), Mock()}, {Color.GREEN}),
        ({Mock(), Mock()}, {Color.RED}),
    ],
)
def test_road_building(activating_hand, receiving_colors_on_board):
    road_building = RoadBuildingDogma()
    assert road_building.symbol == SymbolType.CASTLE

    red_card = Mock()
    green_card = Mock()

    activating_player = Mock(
        hand=activating_hand,
        board={Color.RED: Mock(top_card=red_card)},
        colors_with_cards={Color.RED},
    )
    target_player = (
        Mock(
            board={Color.GREEN: Mock(top_card=green_card)},
            colors_with_cards={Color.GREEN},
        )
        if Color.GREEN in receiving_colors_on_board
        else Mock(
            board={color: Mock(top_card=Mock()) for color in receiving_colors_on_board},
            colors_with_cards=receiving_colors_on_board,
        )
    )
    game_state = Mock(players={activating_player, target_player})

    effect = road_building.dogma_effect(game_state, activating_player)
    if not activating_hand:
        assert effect is None
    else:
        assert isinstance(effect, Meld)
        assert (
            effect.allowed_cards(game_state, activating_player, None) == activating_hand
        )
        assert effect.min_cards == 1
        assert effect.max_cards == 2

        melded_cards = set(list(activating_hand)[:2])
        on_completion = effect.on_completion(melded_cards)

        if len(melded_cards) != 2:
            assert on_completion is None
        else:
            assert isinstance(on_completion, Optional)
            operation = on_completion.operation
            assert isinstance(operation, ExchangeCards)
            assert operation.allowed_giving_player == {activating_player}
            assert operation.allowed_receiving_player == {target_player}
            assert operation.allowed_giving_cards(
                game_state, activating_player, target_player
            ) == {red_card}
            allowed_receiving_cards = operation.allowed_receiving_cards(
                game_state, activating_player, target_player
            )
            assert allowed_receiving_cards == (
                {green_card} if Color.GREEN in receiving_colors_on_board else {}
            )
            assert operation.num_cards_giving == 1
            assert operation.num_cards_receiving == 1
            assert operation.giving_location == CardLocation.BOARD
            assert operation.receiving_location == CardLocation.BOARD
