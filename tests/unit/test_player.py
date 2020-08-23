from src.innovation.cards.cards import GLOBAL_CARD_REGISTRY
from src.innovation.players.players import Player
from src.innovation.cards.card_properties import Color


def test_player_board_meld_single_card():
    archery = GLOBAL_CARD_REGISTRY.registry.get("Archery")
    player = Player(dict(), {archery}, set())
    assert archery in player.hand

    player.meld(archery)

    red_stack = player.board[Color.RED].stack
    assert len(red_stack) == 1
    assert red_stack.pop() == archery
    assert archery not in player.hand
