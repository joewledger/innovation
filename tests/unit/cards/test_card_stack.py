from src.innovation.cards.cards import (
    CardStack,
    Symbol,
    SymbolType,
    Position,
    SplayDirection,
)
from collections import deque
import pytest
from mock import Mock


@pytest.mark.parametrize(
    "cards, splay_direction, expected_symbols",
    [
        ([], SplayDirection.NONE, {}),
        (
            [
                Mock(
                    symbols=[
                        Symbol(SymbolType.CROWN, Position.BOTTOM_LEFT),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_MIDDLE),
                        Symbol(SymbolType.LEAF, Position.BOTTOM_RIGHT),
                    ]
                )
            ],
            SplayDirection.NONE,
            {SymbolType.CROWN: 1, SymbolType.LEAF: 2},
        ),
        (
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
            ],
            SplayDirection.NONE,
            {
                SymbolType.CASTLE: 3,
            },
        ),
        (
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
            ],
            SplayDirection.LEFT,
            {SymbolType.CASTLE: 3, SymbolType.LEAF: 1},
        ),
        (
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
            ],
            SplayDirection.RIGHT,
            {SymbolType.CASTLE: 3, SymbolType.CROWN: 1},
        ),
        (
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
            ],
            SplayDirection.UP,
            {SymbolType.CASTLE: 3, SymbolType.CROWN: 1, SymbolType.LEAF: 2},
        ),
    ],
)
def test_symbol_count(cards, splay_direction, expected_symbols):
    stack = CardStack(deque(cards), splay_direction)
    actual_symbols = stack.symbol_count

    for symbol, count in expected_symbols.items():
        assert actual_symbols[symbol] == count

    for symbol, count in actual_symbols.items():
        if symbol not in expected_symbols:
            assert count == 0
