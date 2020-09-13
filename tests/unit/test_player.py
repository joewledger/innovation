from src.innovation.cards.card_registry import GLOBAL_CARD_REGISTRY
from src.innovation.players.players import Player
from src.innovation.cards.cards import (
    Color,
    CardStack,
    SplayDirection,
    Symbol,
    SymbolType,
    Position,
    get_highest_cards,
)
from collections import deque
import pytest
from mock import Mock


@pytest.mark.parametrize(
    "card_names", [["Archery"], ["Archery", "Sailing"], ["Sailing", "The Wheel"]]
)
def test_player_board_valid_melds(card_names):
    # Given
    cards = [GLOBAL_CARD_REGISTRY.registry.get(card_name) for card_name in card_names]
    player = Player(0, dict(), set(cards), set(), set())
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


@pytest.mark.parametrize(
    "score_pile_cards, expected_score",
    [
        ([], 0),
        ([Mock(age=2)], 2),
        ([Mock(age=2), Mock(age=6)], 8),
        ([Mock(age=n) for n in range(10)], 45),
    ],
)
def test_player_score(score_pile_cards, expected_score):
    player = Player(0, {}, set(), set(score_pile_cards), set())
    assert player.score == expected_score


@pytest.mark.parametrize(
    "cards, expected_max_age",
    [
        ([], 1),
        ([Mock(color=Color.GREEN, age=2)], 2),
        ([Mock(color=Color.RED, age=5)], 5),
        ([Mock(color=Color.GREEN, age=2), Mock(color=Color.RED, age=5)], 5),
        ([Mock(color=Color.RED, age=2), Mock(color=Color.RED, age=5)], 5),
        ([Mock(color=Color.RED, age=5), Mock(color=Color.RED, age=2)], 2),
    ],
)
def test_player_max_age_cards(cards, expected_max_age):
    player = Player(0, {}, set(cards), set(), set())
    for card in cards:
        player.meld(card)

    assert player.max_age_top_card == expected_max_age


@pytest.mark.parametrize(
    "board, expected_symbols",
    [
        ({}, {}),
        (
            {
                Color.GREEN: CardStack(
                    stack=deque(
                        [
                            Mock(
                                symbols=[
                                    Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
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
                        ]
                    ),
                    splay=SplayDirection.UP,
                )
            },
            {SymbolType.CASTLE: 3, SymbolType.CROWN: 1, SymbolType.LEAF: 2},
        ),
        (
            {
                Color.GREEN: CardStack(
                    stack=deque(
                        [
                            Mock(
                                symbols=[
                                    Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
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
                        ]
                    ),
                    splay=SplayDirection.UP,
                ),
                Color.BLUE: CardStack(
                    stack=deque(
                        [
                            Mock(
                                symbols=[
                                    Symbol(SymbolType.LIGHT_BULB, Position.BOTTOM_LEFT),
                                    Symbol(
                                        SymbolType.LIGHT_BULB, Position.BOTTOM_MIDDLE
                                    ),
                                    Symbol(SymbolType.CASTLE, Position.BOTTOM_RIGHT),
                                ]
                            ),
                        ]
                    ),
                    splay=SplayDirection.NONE,
                ),
            },
            {
                SymbolType.CASTLE: 4,
                SymbolType.CROWN: 1,
                SymbolType.LEAF: 2,
                SymbolType.LIGHT_BULB: 2,
            },
        ),
    ],
)
def test_symbol_count(board, expected_symbols):
    player = Player(0, board, set(), set(), set())
    actual_symbols = player.symbol_count

    for symbol, count in expected_symbols.items():
        assert actual_symbols[symbol] == count

    for symbol, count in actual_symbols.items():
        if symbol not in expected_symbols:
            assert count == 0


@pytest.mark.parametrize(
    "board, expected_splayable_colors",
    [
        ({}, set()),
        ({Color.RED: CardStack(deque([Mock()]), SplayDirection.NONE)}, set()),
        (
            {
                Color.RED: CardStack(deque([Mock()]), SplayDirection.NONE),
                Color.YELLOW: CardStack(deque([Mock()]), SplayDirection.NONE),
            },
            set(),
        ),
        (
            {
                Color.RED: CardStack(deque([Mock(), Mock()]), SplayDirection.LEFT),
                Color.YELLOW: CardStack(deque([Mock()]), SplayDirection.NONE),
            },
            {Color.RED},
        ),
        (
            {
                Color.RED: CardStack(deque([Mock(), Mock()]), SplayDirection.RIGHT),
                Color.YELLOW: CardStack(deque([Mock(), Mock()]), SplayDirection.UP),
            },
            {Color.RED, Color.YELLOW},
        ),
    ],
)
def test_splayable_colors(board, expected_splayable_colors):
    player = Player(0, board, set(), set(), set())
    assert player.splayable_colors == expected_splayable_colors


@pytest.mark.parametrize(
    "hand, expected_age, expected_num_cards",
    [
        (set(), None, 0),
        ({Mock(age=1)}, 1, 1),
        ({Mock(age=5)}, 5, 1),
        ({Mock(age=5), Mock(age=1)}, 5, 1),
        ({Mock(age=5), Mock(age=5), Mock(age=1)}, 5, 2),
    ],
)
def test_highest_cards_in_hand(hand, expected_age, expected_num_cards):
    player = Player(0, {}, hand, set(), set())
    highest_cards = get_highest_cards(player.hand)

    assert len(highest_cards) == expected_num_cards
    assert all(card.age == list(highest_cards)[0].age for card in highest_cards)
    if expected_age:
        assert list(highest_cards)[0].age == expected_age
