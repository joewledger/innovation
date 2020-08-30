from src.innovation.cards.achievements import Achievement
from src.innovation.cards.cards import Card
from src.innovation.players.players import Player
from dataclasses import dataclass
from typing import Deque, Dict, Set


@dataclass
class GameState:
    draw_decks: Dict[int, Deque[Card]]
    unclaimed_achievements: Set[Achievement]
    players: Set[Player]
