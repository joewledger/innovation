from src.innovation.cards.card_registry import (
    EngineeringDemand,
    EngineeringDogma,
    OpticsDogma,
    MachineryDemand,
    MachineryDogma,
    MedicineDemand,
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
)
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
        assert effect.num_cards_giving == len(get_lowest_cards(activating_score_pile))
        assert effect.num_cards_receiving == len(get_highest_cards(target_score_pile))
        assert effect.giving_location == CardLocation.SCORE_PILE
        assert effect.receiving_location == CardLocation.SCORE_PILE
