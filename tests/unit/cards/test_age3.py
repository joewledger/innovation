from src.innovation.cards.card_registry import (
    EngineeringDemand,
    EngineeringDogma,
    OpticsDogma,
)
from src.innovation.cards.cards import SymbolType, Color, SplayDirection
from src.innovation.cards.card_effects import (
    Draw,
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
