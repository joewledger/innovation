from src.innovation.cards.achievement_registry import GLOBAL_ACHIEVEMENTS_REGISTRY
from src.innovation.cards.card_registry import GLOBAL_CARD_REGISTRY
from src.innovation.cards.cards import Card
from src.innovation.players.players import Player
from src.innovation.game.gamestate import GameState
from collections import deque
from random import shuffle
from typing import Dict, Deque


def initialize_gamestate(num_players: int) -> GameState:
    draw_decks = initialize_draw_decks()
    unclaimed_achievements = set(GLOBAL_ACHIEVEMENTS_REGISTRY.registry.values())
    players = {
        Player({}, {draw_decks[1].pop(), draw_decks[1].pop()}, set(), set())
        for _ in range(num_players)
    }

    game_state = GameState(draw_decks, unclaimed_achievements, players)

    return game_state


def initialize_draw_decks() -> Dict[int, Deque[Card]]:
    cards = GLOBAL_CARD_REGISTRY.registry.values()
    draw_decks = {}

    for age in range(1, 10):
        cards_in_age = [card for card in cards if card.age == age]
        shuffle(cards_in_age)

        draw_decks[age] = deque(cards_in_age)

    return draw_decks
