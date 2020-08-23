from src.innovation.cards.cards import Card, CardStack
from src.innovation.cards.card_properties import Color, SplayDirection
from collections import deque
from dataclasses import dataclass
from typing import Set, Dict


@dataclass
class Player:
    board: Dict[Color, CardStack]
    hand: Set[Card]
    score_pile: Set[Card]

    @property
    def score(self) -> int:
        return sum(card.age for card in self.score_pile)

    @property
    def max_age_top_card(self) -> int:
        return -1

    def meld(self, card: Card):
        color = card.color

        if color not in self.board:
            self.board[color] = CardStack(deque(), SplayDirection.NONE)

        self.board[color].stack.append(card)
        self.hand.remove(card)
