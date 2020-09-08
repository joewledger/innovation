from src.innovation.cards.card_registry import (
    ConstructionDemand,
    ConstructionDogma,
    RoadBuildingDogma,
    CanalBuildingDogma,
    FermentingDogma,
    CurrencyDogma,
    MapmakingDemand,
    CalendarDogma,
    MathematicsDogma,
    MonotheismDemand,
    MonotheismDogma,
)
from src.innovation.cards.cards import SymbolType, Color
from src.innovation.cards.card_effects import (
    Achieve,
    Draw,
    TransferCard,
    CardLocation,
    Meld,
    Return,
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


@pytest.mark.parametrize(
    "hand_ages, expected_draws",
    [([], 0), ([1], 1), ([1, 2], 2), ([1, 1, 2], 2), ([1, 1, 2, 2, 3], 3)],
)
def test_currency_dogma(hand_ages, expected_draws):
    currency = CurrencyDogma()
    assert currency.symbol == SymbolType.CROWN

    hand = {Mock(age=age) for age in hand_ages}
    activating_player = Mock(hand=hand)
    effect = currency.dogma_effect(Mock(), activating_player)

    if not expected_draws:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Return)
        assert operation.allowed_cards(Mock(), activating_player, None) == hand
        assert operation.min_cards == 1
        assert operation.max_cards == len(hand)

        on_completion = operation.on_completion(hand)
        assert isinstance(on_completion, Draw)
        assert on_completion.target_player == activating_player
        assert on_completion.draw_location(hand) == CardLocation.SCORE_PILE
        assert on_completion.level == 2
        assert on_completion.num_cards == expected_draws


@pytest.mark.parametrize(
    "target_score_pile_ages, should_transfer",
    [([], False), ([1], True), ([2], False), ([1, 2], True)],
)
def test_mapmaking_demand(target_score_pile_ages, should_transfer):
    mapmaking = MapmakingDemand()
    assert mapmaking.symbol == SymbolType.CROWN

    target_score_pile = {Mock(age=age) for age in target_score_pile_ages}
    activating_player = Mock()
    target_player = Mock(score_pile=target_score_pile)

    effect = mapmaking.demand_effect(Mock(), activating_player, target_player)
    chained_dogma = mapmaking.chained_dogma(Mock(), activating_player, [effect])
    if not should_transfer:
        assert effect is None
        assert chained_dogma is None
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.receiving_player == activating_player
        assert effect.allowed_cards(Mock(), activating_player, target_player) == {
            card for card in target_score_pile if card.age == 1
        }
        assert effect.card_location == CardLocation.SCORE_PILE
        assert effect.card_destination == CardLocation.SCORE_PILE

        assert isinstance(chained_dogma, Draw)
        assert chained_dogma.target_player == activating_player
        assert chained_dogma.draw_location(Mock()) == CardLocation.SCORE_PILE
        assert chained_dogma.level == 1


@pytest.mark.parametrize(
    "hand_size, score_pile_size, should_draw",
    [(0, 0, False), (0, 3, True), (4, 0, False), (2, 2, False)],
)
def test_calendar_dogma(hand_size, score_pile_size, should_draw):
    calendar = CalendarDogma()
    assert calendar.symbol == SymbolType.LEAF

    activating_player = Mock(
        hand={Mock() for _ in range(hand_size)},
        score_pile={Mock() for _ in range(score_pile_size)},
    )

    effect = calendar.dogma_effect(Mock(), activating_player)
    if not should_draw:
        assert effect is None
    else:
        assert isinstance(effect, Draw)
        assert effect.target_player == activating_player
        assert effect.draw_location(Mock()) == CardLocation.HAND
        assert effect.level == 3
        assert effect.num_cards == 2


@pytest.mark.parametrize(
    "hand_ages, expected_meld_level", [({}, None), ({1}, 2), ({1, 1}, 2), ({3, 4}, 5)]
)
def test_mathematics_dogma(hand_ages, expected_meld_level):
    mathematics = MathematicsDogma()
    assert mathematics.symbol == SymbolType.LIGHT_BULB

    hand = {Mock(age=age) for age in hand_ages}
    returned_card = max(hand, key=lambda c: c.age) if hand else None
    activating_player = Mock(hand=hand)
    effect = mathematics.dogma_effect(Mock(), activating_player)

    if not expected_meld_level:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Return)

        assert operation.allowed_cards(Mock(), activating_player, None) == hand
        assert operation.min_cards == 1
        assert operation.max_cards == 1

        on_completion = operation.on_completion({returned_card})
        assert isinstance(on_completion, Draw)
        assert on_completion.target_player == activating_player
        assert on_completion.draw_location(Mock()) == CardLocation.BOARD
        assert on_completion.level == returned_card.age + 1


@pytest.mark.parametrize(
    "target_colors, activating_colors, should_transfer",
    [
        (set(), set(), False),
        ({Color.RED}, set(), True),
        ({Color.RED}, {Color.RED}, False),
        ({Color.RED, Color.YELLOW}, {Color.RED}, True),
    ],
)
def test_monotheism_demand(target_colors, activating_colors, should_transfer):
    monotheism = MonotheismDemand()
    assert monotheism.symbol == SymbolType.CASTLE

    activating_player = Mock(colors_with_cards=activating_colors)
    target_top_cards = {Mock(color=color) for color in target_colors}
    target_player = Mock(colors_with_cards=target_colors, top_cards=target_top_cards)

    effect = monotheism.demand_effect(Mock(), activating_player, target_player)
    if not should_transfer:
        assert effect is None
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.receiving_player == activating_player
        assert effect.allowed_cards(Mock(), activating_player, target_player) == {
            card
            for card in target_top_cards
            if card.color in target_colors - activating_colors
        }
        assert effect.card_location == CardLocation.BOARD
        assert effect.card_destination == CardLocation.SCORE_PILE

        on_completion = effect.on_completion(Mock())
        assert isinstance(on_completion, Draw)
        assert on_completion.target_player == target_player
        assert on_completion.draw_location(Mock()) == CardLocation.BOARD
        assert on_completion.level == 1
        assert on_completion.tuck is True


def test_monotheism_dogma():
    monotheism = MonotheismDogma()
    assert monotheism.symbol == SymbolType.CASTLE

    activating_player = Mock()
    effect = monotheism.dogma_effect(Mock(), activating_player)

    assert isinstance(effect, Draw)
    assert effect.target_player == activating_player
    assert effect.draw_location(Mock()) == CardLocation.BOARD
    assert effect.level == 1
    assert effect.tuck is True
