from src.innovation.cards.card_registry import GLOBAL_CARD_REGISTRY
from src.innovation.players.players import Player
from src.innovation.cards.cards import Color
import pytest
from mock import Mock


@pytest.mark.parametrize(
    "card_names", [["Archery"], ["Archery", "Sailing"], ["Sailing", "The Wheel"]]
)
def test_player_board_valid_melds(card_names):
    # Given
    cards = [GLOBAL_CARD_REGISTRY.registry.get(card_name) for card_name in card_names]
    player = Player(dict(), set(cards), set(), set())
    assert all(card in player.hand for card in cards)

    # When
    for card in cards:
        player.meld(card)

    # Then
    card_colors = {card.color for card in cards}

    for card_color in card_colors:
        card_stack = player.board[card_color].stack
        original_cards_of_color = [card for card in cards if card.color == card_color]

        # Check that each board stack is the expected size
        assert len(card_stack) == len(original_cards_of_color)

        # Check that cards are in the correct order in the stack
        melded_cards = [card_stack.popleft() for _ in range(len(card_stack))]
        assert melded_cards == original_cards_of_color

    assert all(card not in player.hand for card in cards)


@pytest.mark.parametrize("score_pile_cards, expected_score", [
    ([], 0),
    ([Mock(age=2)], 2),
    ([Mock(age=2), Mock(age=6)], 8),
    ([Mock(age=n) for n in range(10)], 45)
])
def test_player_score(score_pile_cards, expected_score):
    player = Player({}, set(), set(score_pile_cards), set())
    assert player.score == expected_score


@pytest.mark.parametrize("cards, expected_max_age", [
    ([], 1),
    ([Mock(color=Color.GREEN, age=2)], 2),
    ([Mock(color=Color.RED, age=5)], 5),
    ([Mock(color=Color.GREEN, age=2), Mock(color=Color.RED, age=5)], 5),
    ([Mock(color=Color.RED, age=2), Mock(color=Color.RED, age=5)], 5),
    ([Mock(color=Color.RED, age=5), Mock(color=Color.RED, age=2)], 2)
])
def test_player_max_age_cards(cards, expected_max_age):
    player = Player({}, set(cards), set(), set())
    for card in cards:
        player.meld(card)

    assert player.max_age_top_card == expected_max_age