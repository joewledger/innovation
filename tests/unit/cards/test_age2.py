from src.innovation.cards.card_registry import (
    ConstructionDemand,
    ConstructionDogma,
    RoadBuildingDogma,
    CanalBuildingDogma,
    FermentingDogma,
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


def canal_building_card_sets():
    return [
        set(),
        {Mock(age=1)},
        {Mock(age=2), Mock(age=1)},
        {Mock(age=2), Mock(age=1), Mock(age=1)},
        {Mock(age=2), Mock(age=2), Mock(age=1)},
    ]


@pytest.mark.parametrize("hand", canal_building_card_sets())
@pytest.mark.parametrize("score_pile", canal_building_card_sets())
def test_canal_building(hand, score_pile):
    canal_building = CanalBuildingDogma()
    assert canal_building.symbol == SymbolType.CROWN

    activating_player = Mock(hand=hand, score_pile=score_pile)

    effect = canal_building.dogma_effect(Mock(), activating_player)
    if not hand and not score_pile:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, ExchangeCards)
        assert operation.allowed_giving_player == {activating_player}
        assert operation.allowed_receiving_player == {activating_player}
        assert operation.allowed_giving_cards(Mock(), activating_player, None) == {
            card for card in hand if card.age == max(hand, key=lambda c: c.age)
        }
        assert operation.allowed_receiving_cards(Mock(), activating_player, None) == {
            card
            for card in score_pile
            if card.age == max(score_pile, key=lambda c: c.age)
        }
        assert operation.num_cards_giving == len(
            {card for card in hand if card.age == max(hand, key=lambda c: c.age)}
        )
        assert operation.num_cards_receiving == len(
            {
                card
                for card in score_pile
                if card.age == max(score_pile, key=lambda c: c.age)
            }
        )
        assert operation.giving_location == CardLocation.HAND
        assert operation.receiving_location == CardLocation.SCORE_PILE


@pytest.mark.parametrize(
    "num_leafs, expected_draws", [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (11, 5)]
)
def test_fermenting(num_leafs, expected_draws):
    fermenting = FermentingDogma()
    assert fermenting.symbol == SymbolType.LEAF

    activating_player = Mock(symbol_count={SymbolType.LEAF: num_leafs})

    effect = fermenting.dogma_effect(Mock(), activating_player)

    if not expected_draws:
        assert effect is None
    else:
        assert isinstance(effect, Draw)
        assert effect.target_player == activating_player
        assert effect.draw_location(Mock()) == CardLocation.HAND
        assert effect.level == 2
        assert effect.num_cards == expected_draws
