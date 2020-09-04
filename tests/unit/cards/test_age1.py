from src.innovation.cards.card_registry import (
    ArcheryDemand,
    CityStatesDemand,
    OarsDemand,
    MetalWorkingDogma,
    AgricultureDogma,
    DomesticationDogma,
    MasonryDogma,
    ClothingDogma1,
    ClothingDogma2,
    SailingDogma,
    WheelDogma,
    PotteryDogma1,
    PotteryDogma2,
    ToolsDogma1,
    ToolsDogma2,
    WritingDogma,
)
from src.innovation.cards.cards import SymbolType, Symbol, Position, Color
from src.innovation.cards.card_effects import (
    Draw,
    Meld,
    Achieve,
    CardLocation,
    TransferCard,
    Optional,
    Return,
)
from mock import Mock
import pytest
from random import choice


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
    "target_player_transferable_hand, target_player_non_transferable_hand, should_transfer",
    [
        (set(), set(), False),
        (
            set(),
            {Mock(symbols=[Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT)])},
            False,
        ),
        ({Mock(symbols=[Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT)])}, set(), True),
    ],
)
def test_oars_demand(
    target_player_transferable_hand,
    target_player_non_transferable_hand,
    should_transfer,
):
    oars_demand = OarsDemand()
    assert oars_demand.symbol == SymbolType.CASTLE

    game_state = Mock()
    target_player = Mock(
        hand=target_player_transferable_hand.union(target_player_non_transferable_hand)
    )
    activating_player = Mock()

    effect = oars_demand.demand_effect(game_state, activating_player, target_player)
    if not should_transfer:
        assert effect is None
    else:
        transferred_card = Mock()

        assert effect.giving_player == target_player
        assert effect.receiving_player == activating_player
        assert (
            effect.allowed_cards(game_state, activating_player, target_player)
            == target_player_transferable_hand
        )
        assert effect.card_location == CardLocation.HAND
        assert effect.card_destination == CardLocation.SCORE_PILE

        on_completion_effect = effect.on_completion(transferred_card)
        assert isinstance(on_completion_effect, Draw)

        drawn_card = Mock()
        assert on_completion_effect.target_player == target_player
        assert on_completion_effect.draw_location(drawn_card) == CardLocation.HAND
        assert on_completion_effect.level == 1


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
        transferred_card = Mock()
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

        on_completion_effect = effect.on_completion(transferred_card)
        assert isinstance(on_completion_effect, Draw)
        assert on_completion_effect.target_player == target_player
        assert on_completion_effect.draw_location(drawn_card) == CardLocation.HAND
        assert on_completion_effect.level == 1


@pytest.mark.parametrize(
    "drawn_card, draw_location, should_repeat",
    [
        (
            Mock(symbols=[Symbol(SymbolType.CASTLE, Position.TOP_LEFT)]),
            CardLocation.SCORE_PILE,
            True,
        ),
        (
            Mock(symbols=[Symbol(SymbolType.LEAF, Position.TOP_LEFT)]),
            CardLocation.HAND,
            False,
        ),
    ],
)
def test_metalworking_dogma(drawn_card, draw_location, should_repeat):
    metalworking = MetalWorkingDogma()
    assert metalworking.symbol == SymbolType.CASTLE

    game_state = Mock()
    activating_player = Mock()

    effect = metalworking.dogma_effect(game_state, activating_player)
    assert isinstance(effect, Draw)
    assert effect.target_player == activating_player
    assert effect.draw_location({drawn_card}) == draw_location
    assert effect.repeat_effect({drawn_card}) == should_repeat
    assert effect.level == 1
    assert effect.reveal is True
    assert effect.num_cards == 1
    assert effect.on_completion is None


@pytest.mark.parametrize("hand", [set(), {Mock(age=1)}, {Mock(age=2), Mock(age=3)}])
def test_agriculture(hand):
    agriculture = AgricultureDogma()
    assert agriculture.symbol == SymbolType.LEAF

    game_state = Mock()
    activating_player = Mock(hand=hand)

    effect = agriculture.dogma_effect(game_state, activating_player)

    if not hand:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Return)

        returned_card = max(hand, key=lambda card: card.age)

        assert operation.allowed_cards(game_state, activating_player, None) == hand
        assert operation.min_cards == 1
        assert operation.max_cards == 1

        on_completion_effect = operation.on_completion({returned_card})
        assert isinstance(on_completion_effect, Draw)

        drawn_card = Mock()
        assert on_completion_effect.target_player == activating_player
        assert on_completion_effect.draw_location(drawn_card) == CardLocation.SCORE_PILE
        assert on_completion_effect.level == returned_card.age + 1


@pytest.mark.parametrize(
    "hand",
    [
        {},
        {Mock(age=1)},
        {Mock(age=2), Mock(age=3)},
        {Mock(age=2), Mock(age=2), Mock(age=3)},
    ],
)
def test_domestication(hand):
    domestication = DomesticationDogma()

    game_state = Mock()
    activating_player = Mock(hand=hand)

    effect = domestication.dogma_effect(game_state, activating_player)

    def validate_draw(d: Draw):
        drawn_card = Mock()

        assert isinstance(d, Draw)
        assert d.target_player == activating_player
        assert d.draw_location(drawn_card) == CardLocation.HAND
        assert d.level == 1

    if not hand:
        validate_draw(effect)
    else:
        assert isinstance(effect, Meld)

        lowest_card = {
            card for card in hand if card.age == min(hand, key=lambda c: c.age).age
        }
        assert effect.allowed_cards(game_state, activating_player, None) == lowest_card
        assert effect.min_cards == 1
        assert effect.max_cards == 1

        melded_card = Mock()
        draw = effect.on_completion(melded_card)
        validate_draw(draw)


@pytest.mark.parametrize(
    "meldable_cards, non_meldable_cards",
    [
        (set(), set()),
        (set(), {Mock(symbols=[Symbol(SymbolType.LEAF, Position.BOTTOM_LEFT)])}),
        ({Mock(symbols=[Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT)])}, set()),
        (
            {
                Mock(symbols=[Symbol(SymbolType.CASTLE, Position.BOTTOM_LEFT)]),
                Mock(symbols=[Symbol(SymbolType.CASTLE, Position.TOP_LEFT)]),
                Mock(symbols=[Symbol(SymbolType.CASTLE, Position.BOTTOM_MIDDLE)]),
                Mock(symbols=[Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT)]),
            },
            set(),
        ),
    ],
)
def test_masonry(meldable_cards, non_meldable_cards):
    masonry = MasonryDogma()
    assert masonry.symbol == SymbolType.CASTLE

    hand = meldable_cards.union(non_meldable_cards)
    game_state = Mock()
    activating_player = Mock(hand=hand)

    effect = masonry.dogma_effect(game_state, activating_player)
    if not meldable_cards:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Meld)
        assert operation.min_cards == 1
        assert operation.max_cards == len(meldable_cards)
        assert (
            operation.allowed_cards(game_state, activating_player, None)
            == meldable_cards
        )

        on_completion = operation.on_completion(meldable_cards)
        if len(meldable_cards) >= 4:
            assert isinstance(on_completion, Achieve)
            assert on_completion.achievement.name == "Monument"
        else:
            assert on_completion is None


@pytest.mark.parametrize(
    "allowed_meld, disallowed_meld, colors_with_cards",
    [
        (set(), set(), set()),
        ({Mock(color=Color.RED)}, set(), set()),
        ({Mock(color=Color.RED)}, {Mock(color=Color.YELLOW)}, {Color.YELLOW}),
        (
            set(),
            {Mock(color=Color.YELLOW), Mock(color=Color.RED)},
            {Color.YELLOW, Color.RED},
        ),
    ],
)
def test_clothing_dogma1(allowed_meld, disallowed_meld, colors_with_cards):
    clothing = ClothingDogma1()
    assert clothing.symbol == SymbolType.LEAF

    hand = allowed_meld.union(disallowed_meld)

    game_state = Mock()
    activating_player = Mock(hand=hand, colors_with_cards=colors_with_cards)
    effect = clothing.dogma_effect(game_state, activating_player)

    if not allowed_meld:
        assert effect is None
    else:
        assert isinstance(effect, Meld)
        assert effect.min_cards == 1
        assert effect.max_cards == 1
        assert effect.allowed_cards(game_state, activating_player, None) == allowed_meld
        assert effect.on_completion is None


@pytest.mark.parametrize(
    "colors, opposing_player_colors, num_draws",
    [
        (set(), [set()], 0),
        ({Color.RED}, [set()], 1),
        ({Color.RED, Color.YELLOW}, [set()], 2),
        ({Color.RED, Color.YELLOW}, [{Color.RED}], 1),
        ({Color.RED, Color.YELLOW}, [{Color.RED}, {Color.YELLOW}], 0),
        (
            {Color.RED, Color.YELLOW, Color.BLUE},
            [{Color.RED, Color.YELLOW}, {Color.YELLOW}],
            1,
        ),
    ],
)
def test_clothing_dogma2(colors, opposing_player_colors, num_draws):
    clothing = ClothingDogma2()
    assert clothing.symbol == SymbolType.LEAF

    opposing_players = {
        Mock(colors_with_cards=player_colors)
        for player_colors in opposing_player_colors
    }
    activating_player = Mock(colors_with_cards=colors)

    game_state = Mock(players=opposing_players | {activating_player})

    effect = clothing.dogma_effect(game_state, activating_player)
    if num_draws == 0:
        assert effect is None
    else:
        assert isinstance(effect, Draw)
        drawn_card = Mock()

        assert effect.target_player == activating_player
        assert effect.draw_location(drawn_card) == CardLocation.SCORE_PILE
        assert effect.level == 1
        assert effect.num_cards == num_draws


def test_sailing():
    sailing = SailingDogma()
    assert sailing.symbol == SymbolType.CROWN

    game_state = Mock()
    activating_player = Mock()

    effect = sailing.dogma_effect(game_state, activating_player)
    assert isinstance(effect, Draw)

    drawn_card = Mock()
    assert effect.target_player == activating_player
    assert effect.draw_location(drawn_card) == CardLocation.BOARD
    assert effect.level == 1


def test_wheel():
    wheel = WheelDogma()
    assert wheel.symbol == SymbolType.CASTLE

    game_state = Mock()
    activating_player = Mock()

    effect = wheel.dogma_effect(game_state, activating_player)
    assert isinstance(effect, Draw)
    draw2 = effect.on_completion(Mock())
    assert isinstance(draw2, Draw)

    assert effect.target_player == draw2.target_player == activating_player
    assert (
        effect.draw_location(Mock()) == draw2.draw_location(Mock()) == CardLocation.HAND
    )
    assert effect.level == draw2.level == 1


@pytest.mark.parametrize(
    "hand, num_cards_to_return",
    [(set(), 0), ({Mock()}, 1), ({Mock() for _ in range(5)}, 3)],
)
def test_pottery_dogma1(hand, num_cards_to_return):
    pottery = PotteryDogma1()
    assert pottery.symbol == SymbolType.LEAF

    activating_player = Mock(hand=hand)
    effect = pottery.dogma_effect(Mock(), activating_player)

    if not hand:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation

        assert isinstance(operation, Return)
        assert operation.allowed_cards(Mock(), activating_player, None) == hand
        assert operation.min_cards == 1
        assert operation.max_cards == 3

        on_completion = operation.on_completion(set(list(hand)[:num_cards_to_return]))
        assert isinstance(on_completion, Draw)
        assert on_completion.target_player == activating_player
        assert on_completion.draw_location(Mock()) == CardLocation.SCORE_PILE
        assert on_completion.level == num_cards_to_return


def test_pottery_dogma2():
    pottery = PotteryDogma2()
    assert pottery.symbol == SymbolType.LEAF

    activating_player = Mock()

    effect = pottery.dogma_effect(Mock(), activating_player)
    assert isinstance(effect, Draw)
    assert effect.target_player == activating_player
    assert effect.draw_location(Mock()) == CardLocation.HAND
    assert effect.level == 1


def test_tools_dogma1():
    pass


def test_tools_dogma2():
    pass


def test_writing():
    writing = WritingDogma()
    assert writing.symbol == SymbolType.LIGHT_BULB

    activating_player = Mock()
    effect = writing.dogma_effect(Mock(), activating_player)
    assert isinstance(effect, Draw)
    assert effect.target_player == activating_player
    assert effect.draw_location(Mock()) == CardLocation.HAND
    assert effect.level == 2
