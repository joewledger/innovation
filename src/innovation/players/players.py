from src.innovation.cards.achievements import Achievement
from src.innovation.cards.cards import (
    Card,
    CardStack,
    Color,
    SplayDirection,
    SymbolType,
)
from collections import deque
from dataclasses import dataclass
from typing import Set, Dict


@dataclass
class Player:
    id: int
    board: Dict[Color, CardStack]
    hand: Set[Card]
    score_pile: Set[Card]
    achievements: Set[Achievement]

    @property
    def score(self) -> int:
        return sum(card.age for card in self.score_pile)

    @property
    def top_cards(self) -> Set[Card]:
        return {
            card_stack.top_card
            for card_stack in self.board.values()
            if not card_stack.is_empty
        }

    @property
    def highest_cards_in_hand(self) -> Set[Card]:
        return {
            card
            for card in self.hand
            if card.age == max(self.hand, key=lambda c: c.age).age
        }

    @property
    def max_age_top_card(self) -> int:
        if len(self.top_cards) == 0:
            return 1

        return max(top_card.age for top_card in self.top_cards)

    @property
    def colors_with_cards(self) -> Set[Color]:
        return {
            color
            for color in self.board.keys()
            if color in self.board and not self.board[color].is_empty()
        }

    @property
    def splayable_colors(self) -> Set[Color]:
        return {color for color in self.board if self.board[color].can_splay}

    @property
    def symbol_count(self) -> Dict[SymbolType, int]:
        card_stacks = self.board.values()
        return {
            symbol_type: sum(
                stack.symbol_count.get(symbol_type, 0) for stack in card_stacks
            )
            for symbol_type in SymbolType
        }

    def meld(self, card: Card):
        color = card.color

        if color not in self.board:
            self.board[color] = CardStack(deque(), SplayDirection.NONE)

        self.board[color].stack.append(card)
        self.hand.remove(card)

    def __eq__(self, other):
        return isinstance(other, Player) and self.id == other.id

    def __hash__(self):
        return self.id
