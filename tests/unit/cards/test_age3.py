from src.innovation.cards.card_registry import (
    EngineeringDemand,
    EngineeringDogma,
    OpticsDogma,
    MachineryDemand,
    MachineryDogma,
    MedicineDemand,
    CompassDemand,
    PaperDogma1,
    PaperDogma2,
    AlchemyDogma1,
    AlchemyDogma2,
    TranslationDogma1,
    TranslationDogma2,
    EducationDogma,
    FeudalismDemand,
    FeudalismDogma,
)
from src.innovation.cards.cards import (
    SymbolType,
    Color,
    SplayDirection,
    get_highest_cards,
    get_lowest_cards,
)
from src.innovation.cards.card_effects import (
    Draw,
    Optional,
    Splay,
    TransferCard,
    CardLocation,
    ExchangeCards,
    Return,
    Meld,
    Score,
    Achieve,
)
from src.innovation.cards.achievement_registry import GLOBAL_ACHIEVEMENTS_REGISTRY
from src.innovation.players.players import Player
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


@pytest.mark.parametrize("drawn_card_has_crown", [True, False])
@pytest.mark.parametrize("activating_player_score", [0, 2, 7])
@pytest.mark.parametrize("other_player_score", [0, 2, 6])
def test_optics_dogma(
    drawn_card_has_crown, activating_player_score, other_player_score
):
    optics = OpticsDogma()
    assert optics.symbol == SymbolType.CROWN

    activating_score_pile = {Mock(age=1) for _ in range(activating_player_score)}
    activating_player = Mock(
        score=activating_player_score, score_pile=activating_score_pile
    )
    other_player = Mock(score=other_player_score)
    game_state = Mock(players={activating_player, other_player})

    drawn_card = Mock(has_symbol_type=lambda _: drawn_card_has_crown)

    effect = optics.dogma_effect(game_state, activating_player)
    assert isinstance(effect, Draw)
    assert effect.target_player == activating_player
    assert effect.draw_location(drawn_card) == CardLocation.BOARD
    assert effect.level == 3

    on_completion = effect.on_completion({drawn_card})
    if drawn_card_has_crown:
        assert isinstance(on_completion, Draw)
        assert on_completion.target_player == activating_player
        assert on_completion.draw_location(Mock()) == CardLocation.SCORE_PILE
        assert on_completion.level == 4
    elif activating_player_score > other_player_score:
        assert isinstance(on_completion, TransferCard)
        assert on_completion.giving_player == activating_player
        assert on_completion.allowed_receiving_players == {other_player}
        assert (
            on_completion.allowed_cards(game_state, activating_player, None)
            == activating_score_pile
        )
        assert on_completion.card_location == CardLocation.SCORE_PILE
        assert on_completion.card_destination == CardLocation.SCORE_PILE
    else:
        assert on_completion is None


@pytest.mark.parametrize(
    "activating_hand, target_hand",
    [
        (set(), set()),
        ({Mock(age=1)}, set()),
        (set(), {Mock(age=1)}),
        ({Mock(age=1)}, {Mock(age=1)}),
        ({Mock(age=2)}, {Mock(age=1)}),
        ({Mock(age=1)}, {Mock(age=2)}),
        ({Mock(age=1), Mock(age=1)}, {Mock(age=2)}),
    ],
)
def test_machinery_demand(activating_hand, target_hand):
    machinery = MachineryDemand()
    assert machinery.symbol == SymbolType.LEAF

    activating_player = Player(0, {}, activating_hand, set(), set())
    target_player = Player(0, {}, target_hand, set(), set())

    highest_activating_cards = get_highest_cards(activating_hand)
    highest_target_cards = get_highest_cards(target_hand)

    effect = machinery.demand_effect(Mock(), activating_player, target_player)

    if not (activating_hand or target_hand):
        assert effect is None
    else:
        assert isinstance(effect, ExchangeCards)
        assert effect.allowed_giving_player == {activating_player}
        assert effect.allowed_receiving_player == {target_player}
        assert (
            effect.allowed_giving_cards(Mock(), activating_player, target_player)
            == highest_activating_cards
        )
        assert (
            effect.allowed_receiving_cards(Mock(), activating_player, target_player)
            == highest_target_cards
        )
        assert effect.num_cards_giving == len(highest_activating_cards)
        assert effect.num_cards_receiving == len(highest_target_cards)
        assert effect.giving_location == CardLocation.HAND
        assert effect.receiving_location == CardLocation.HAND


@pytest.mark.parametrize(
    "hand",
    [
        set(),
        {Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CASTLE)},
        {Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CASTLE)},
        {
            Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CASTLE),
            Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CASTLE),
        },
    ],
)
@pytest.mark.parametrize(
    "splayable_colors", [set(), {Color.RED}, {Color.YELLOW}, {Color.RED, Color.YELLOW}]
)
def test_machinery_dogma(hand, splayable_colors):
    machinery = MachineryDogma()
    assert machinery.symbol == SymbolType.LEAF

    cards_with_castles = {
        card for card in hand if card.has_symbol_type(SymbolType.CASTLE)
    }
    activating_player = Mock(hand=hand, splayable_colors=splayable_colors)

    def validate_splay(optional):
        assert isinstance(optional, Optional)
        splay = optional.operation
        assert isinstance(splay, Splay)
        assert splay.target_player == activating_player
        assert splay.allowed_directions == {SplayDirection.LEFT}
        assert splay.allowed_colors == {Color.RED}

    effect = machinery.dogma_effect(Mock(), activating_player)
    if cards_with_castles:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == activating_player
        assert effect.allowed_receiving_players == {activating_player}
        assert (
            effect.allowed_cards(Mock(), activating_player, None) == cards_with_castles
        )
        assert effect.card_location == CardLocation.HAND
        assert effect.card_destination == CardLocation.SCORE_PILE
        assert effect.num_cards == 1
        validate_splay(effect.on_completion(Mock()))
    elif Color.RED in splayable_colors:
        validate_splay(effect)
    else:
        assert effect is None


@pytest.mark.parametrize(
    "activating_score_pile, target_score_pile",
    [
        (set(), set()),
        ({Mock(age=1)}, set()),
        (set(), {Mock(age=1)}),
        ({Mock(age=1)}, {Mock(age=1)}),
        ({Mock(age=2), Mock(age=2), Mock(age=1)}, {Mock(age=1)}),
        ({Mock(age=1)}, {Mock(age=2), Mock(age=2), Mock(age=1)}),
    ],
)
def test_medicine_demand(activating_score_pile, target_score_pile):
    medicine = MedicineDemand()
    assert medicine.symbol == SymbolType.LEAF

    activating_player = Mock(score_pile=activating_score_pile)
    target_player = Mock(score_pile=target_score_pile)

    effect = medicine.demand_effect(Mock(), activating_player, target_player)

    if not (activating_score_pile or target_score_pile):
        assert effect is None
    else:
        assert isinstance(effect, ExchangeCards)
        assert effect.allowed_giving_player == {activating_player}
        assert effect.allowed_receiving_player == {target_player}
        assert effect.allowed_giving_cards(
            Mock(), activating_player, target_player
        ) == get_lowest_cards(activating_score_pile)
        assert effect.allowed_receiving_cards(
            Mock(), activating_player, target_player
        ) == get_highest_cards(target_score_pile)
        assert effect.num_cards_giving == min(1, len(activating_player.score_pile))
        assert effect.num_cards_receiving == min(1, len(target_player.score_pile))
        assert effect.giving_location == CardLocation.SCORE_PILE
        assert effect.receiving_location == CardLocation.SCORE_PILE


@pytest.mark.parametrize(
    "activating_top_cards",
    [
        set(),
        {Mock(has_symbol_type=lambda symbol: symbol == SymbolType.LEAF)},
        {Mock(has_symbol_type=lambda symbol: symbol != SymbolType.LEAF)},
    ],
)
@pytest.mark.parametrize(
    "target_top_cards",
    [
        set(),
        {
            Mock(
                has_symbol_type=lambda symbol: symbol == SymbolType.LEAF,
                color=Color.RED,
            )
        },
        {
            Mock(
                has_symbol_type=lambda symbol: symbol == SymbolType.LEAF,
                color=Color.GREEN,
            )
        },
        {Mock(has_symbol_type=lambda symbol: symbol != SymbolType.LEAF)},
    ],
)
def test_compass_demand(activating_top_cards, target_top_cards):
    compass = CompassDemand()
    assert compass.symbol == SymbolType.CROWN

    activating_player = Mock(top_cards=activating_top_cards)
    target_player = Mock(top_cards=target_top_cards)

    effect = compass.demand_effect(Mock(), activating_player, target_player)

    target_transferable_cards = {
        card
        for card in target_top_cards
        if card.has_symbol_type(SymbolType.LEAF) and not card.color == Color.GREEN
    }

    activating_transferable_cards = {
        card
        for card in activating_top_cards
        if not card.has_symbol_type(SymbolType.LEAF)
    }

    if not target_transferable_cards and not activating_transferable_cards:
        assert effect is None
    elif target_transferable_cards:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.allowed_receiving_players == {activating_player}
        assert (
            effect.allowed_cards(Mock(), activating_player, target_player)
            == target_transferable_cards
        )
        assert effect.card_location == CardLocation.BOARD
        assert effect.card_destination == CardLocation.BOARD

        on_completion = effect.on_completion(Mock())
        assert isinstance(on_completion, TransferCard)
        assert on_completion.giving_player == activating_player
        assert on_completion.allowed_receiving_players == {target_player}
        assert (
            on_completion.allowed_cards(Mock(), activating_player, target_player)
            == activating_transferable_cards
        )
        assert on_completion.card_location == CardLocation.BOARD
        assert on_completion.card_destination == CardLocation.BOARD
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == activating_player
        assert effect.allowed_receiving_players == {target_player}
        assert (
            effect.allowed_cards(Mock(), activating_player, target_player)
            == activating_transferable_cards
        )
        assert effect.card_location == CardLocation.BOARD
        assert effect.card_destination == CardLocation.BOARD


@pytest.mark.parametrize(
    "splayable_colors, should_splay",
    [
        (set(), False),
        ({Color.RED}, False),
        ({Color.YELLOW}, False),
        ({Color.PURPLE}, False),
        ({Color.GREEN}, True),
        ({Color.BLUE}, True),
        ({Color.GREEN, Color.BLUE}, True),
    ],
)
def test_paper_dogma1(splayable_colors, should_splay):
    paper = PaperDogma1()
    assert paper.symbol == SymbolType.LIGHT_BULB

    activating_player = Mock(splayable_colors=splayable_colors)
    effect = paper.dogma_effect(Mock(), activating_player)

    if not should_splay:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Splay)
        assert operation.target_player == activating_player
        assert operation.allowed_colors == {
            color for color in {Color.GREEN, Color.BLUE} if color in splayable_colors
        }
        assert operation.allowed_directions == {SplayDirection.LEFT}


@pytest.mark.parametrize(
    "board, num_draws",
    [
        ({}, 0),
        ({Color.RED: Mock(splay=SplayDirection.LEFT)}, 1),
        (
            {
                Color.RED: Mock(splay=SplayDirection.LEFT),
                Color.BLUE: Mock(splay=SplayDirection.NONE),
            },
            1,
        ),
        (
            {
                Color.RED: Mock(splay=SplayDirection.LEFT),
                Color.BLUE: Mock(splay=SplayDirection.LEFT),
            },
            2,
        ),
    ],
)
def test_paper_dogma2(board, num_draws):
    paper = PaperDogma2()
    assert paper.symbol == SymbolType.LIGHT_BULB

    activating_player = Mock(board=board)
    effect = paper.dogma_effect(Mock(), activating_player)

    if not num_draws:
        assert effect is None
    else:
        assert isinstance(effect, Draw)
        assert effect.target_player == activating_player
        assert effect.draw_location(Mock()) == CardLocation.HAND
        assert effect.level == 4
        assert effect.num_cards == num_draws


@pytest.mark.parametrize(
    "num_castles, num_draws, drawn_colors",
    [
        (0, 0, set()),
        (1, 0, set()),
        (2, 0, set()),
        (3, 1, {Color.RED}),
        (3, 1, {Color.BLUE}),
        (6, 2, {Color.RED, Color.RED}),
        (6, 2, {Color.BLUE, Color.RED}),
        (6, 2, {Color.BLUE, Color.PURPLE}),
    ],
)
def test_alchemy_dogma1(num_castles, num_draws, drawn_colors):
    alchemy = AlchemyDogma1()
    assert alchemy.symbol == SymbolType.CASTLE

    hand = {Mock() for _ in range(3)}
    activating_player = Mock(hand=hand, symbol_count={SymbolType.CASTLE: num_castles})

    effect = alchemy.dogma_effect(Mock(), activating_player)
    if not num_draws:
        assert effect is None
    else:
        assert isinstance(effect, Draw)
        assert effect.target_player == activating_player

        drawn_cards = {Mock(color=color) for color in drawn_colors}
        red_in_drawn_cards = any(card.color == Color.RED for card in drawn_cards)
        draw_location = effect.draw_location(drawn_cards)
        assert draw_location == (
            CardLocation.DECK if red_in_drawn_cards else CardLocation.HAND
        )

        assert effect.level == 4
        assert effect.num_cards == num_draws
        assert effect.reveal is True

        on_completion = effect.on_completion(drawn_cards)
        if red_in_drawn_cards:
            assert isinstance(on_completion, Return)
            assert on_completion.allowed_cards(Mock(), activating_player, None) == hand
            assert on_completion.min_cards == len(hand)
            assert on_completion.max_cards == len(hand)
        else:
            assert on_completion is None


@pytest.mark.parametrize("hand_size", list(range(3)))
def test_alchemy_dogma2(hand_size):
    alchemy = AlchemyDogma2()
    assert alchemy.symbol == SymbolType.CASTLE

    hand = {Mock() for _ in range(hand_size)}
    activating_player = Mock(hand=hand)
    effect = alchemy.dogma_effect(Mock(), activating_player)

    if not hand_size:
        assert effect is None
    else:
        assert isinstance(effect, Meld)
        assert effect.allowed_cards(Mock(), activating_player, None) == hand
        assert effect.min_cards == 1
        assert effect.max_cards == 1

        melded_card = {list(hand)[0]}
        on_completion = effect.on_completion(melded_card)
        if hand - melded_card:
            assert isinstance(on_completion, Score)
            assert (
                on_completion.allowed_cards(Mock(), activating_player, None)
                == hand - melded_card
            )
        else:
            assert on_completion is None


@pytest.mark.parametrize("score_pile_size", list(range(3)))
def test_translation_dogma1(score_pile_size):
    translation = TranslationDogma1()
    assert translation.symbol == SymbolType.CROWN

    score_pile = {Mock() for _ in range(score_pile_size)}
    activating_player = Mock(score_pile=score_pile)
    effect = translation.dogma_effect(Mock(), activating_player)

    if not score_pile:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Meld)
        assert operation.allowed_cards(Mock(), activating_player, None) == score_pile
        assert operation.min_cards == len(score_pile)
        assert operation.max_cards == len(score_pile)
        assert operation.card_location == CardLocation.SCORE_PILE
        assert operation.card_destination == CardLocation.BOARD


@pytest.mark.parametrize(
    "top_cards, should_achieve",
    [
        (set(), True),
        ({Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CROWN)}, False),
        ({Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CROWN)}, True),
        (
            {
                Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CROWN),
                Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CROWN),
            },
            False,
        ),
        (
            {
                Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CROWN)
                for _ in range(5)
            },
            True,
        ),
    ],
)
def test_translation_dogma2(top_cards, should_achieve):
    translation = TranslationDogma2()
    assert translation.symbol == SymbolType.CROWN

    activating_player = Mock(top_cards=top_cards)
    effect = translation.dogma_effect(Mock(), activating_player)

    if not should_achieve:
        assert effect is None
    else:
        assert isinstance(effect, Achieve)
        assert effect.achievement == GLOBAL_ACHIEVEMENTS_REGISTRY.registry.get("World")


@pytest.mark.parametrize(
    "score_pile_ages, expected_draw_age",
    [(set(), None), ({1}, None), ({1, 1}, 3), ({2, 1}, 3), ({7, 1}, 3), ({7, 4}, 6)],
)
def test_education_dogma(score_pile_ages, expected_draw_age):
    education = EducationDogma()
    assert education.symbol == SymbolType.LIGHT_BULB

    score_pile = {Mock(age=age) for age in score_pile_ages}
    activating_player = Mock(score_pile=score_pile)
    effect = education.dogma_effect(Mock(), activating_player)

    if not score_pile:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Return)
        assert operation.allowed_cards(
            Mock(), activating_player, None
        ) == get_highest_cards(score_pile)
        assert operation.card_location == CardLocation.SCORE_PILE
        assert operation.card_destination == CardLocation.DECK

        returned_cards = {list(get_highest_cards(score_pile))[0]}
        on_completion = operation.on_completion(returned_cards)

        if score_pile - returned_cards:
            assert isinstance(on_completion, Draw)
            assert on_completion.target_player == activating_player
            assert on_completion.draw_location(Mock()) == CardLocation.HAND
            assert (
                on_completion.level
                == list(get_highest_cards(score_pile - returned_cards))[0].age + 2
            )
        else:
            assert on_completion is None


@pytest.mark.parametrize(
    "target_player_hand, should_transfer",
    [
        (set(), False),
        ({Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CASTLE)}, False),
        ({Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CASTLE)}, True),
        (
            {
                Mock(has_symbol_type=lambda symbol: symbol == SymbolType.CASTLE),
                Mock(has_symbol_type=lambda symbol: symbol != SymbolType.CASTLE),
            },
            True,
        ),
    ],
)
def test_feudalism_demand(target_player_hand, should_transfer):
    feudalism = FeudalismDemand()
    assert feudalism.symbol == SymbolType.CASTLE

    activating_player = Mock()
    target_player = Mock(hand=target_player_hand)
    effect = feudalism.demand_effect(Mock(), activating_player, target_player)

    if not should_transfer:
        assert effect is None
    else:
        assert isinstance(effect, TransferCard)
        assert effect.giving_player == target_player
        assert effect.allowed_receiving_players == {activating_player}
        assert effect.allowed_cards(Mock(), activating_player, target_player) == {
            card
            for card in target_player_hand
            if card.has_symbol_type(SymbolType.CASTLE)
        }
        assert effect.card_location == CardLocation.HAND
        assert effect.card_destination == CardLocation.HAND


@pytest.mark.parametrize(
    "splayable_colors",
    [
        set(),
        {Color.RED},
        {Color.YELLOW},
        {Color.PURPLE},
        {Color.RED, Color.BLUE},
        {Color.YELLOW, Color.RED},
        {Color.YELLOW, Color.PURPLE},
    ],
)
def test_feudalism_dogma(splayable_colors):
    feudalism = FeudalismDogma()
    assert feudalism.symbol == SymbolType.CASTLE

    activating_player = Mock(splayable_colors=splayable_colors)
    effect = feudalism.dogma_effect(Mock(), activating_player)

    player_splayable_colors = {Color.YELLOW, Color.PURPLE} & splayable_colors
    if not player_splayable_colors:
        assert effect is None
    else:
        assert isinstance(effect, Optional)
        operation = effect.operation
        assert isinstance(operation, Splay)
        assert operation.target_player == activating_player
        assert operation.allowed_colors == player_splayable_colors
        assert operation.allowed_directions == {SplayDirection.LEFT}
