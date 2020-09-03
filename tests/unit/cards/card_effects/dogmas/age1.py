from src.innovation.cards.card_registry import MetalWorkingDogma
from src.innovation.cards.card_effects import Draw, CardLocation
from src.innovation.cards.cards import Symbol, SymbolType, Position
import pytest
from mock import Mock


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
