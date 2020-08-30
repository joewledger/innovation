from src.innovation.cards.achievements import Achievement
from src.innovation.utils.registry import ImmutableRegistry
from src.innovation.players.players import Player
from functools import partial


def scoring_achievement_condition_met(player: Player, level: int) -> bool:
    return player.score >= level * 5 and player.max_age_top_card >= level


GLOBAL_ACHIEVEMENTS_REGISTRY = ImmutableRegistry(
    [
        Achievement("Monument", True, lambda player: False),
        Achievement("Empire", True, lambda player: False),
        Achievement("Wonder", True, lambda player: False),
        Achievement("World", True, lambda player: False),
        Achievement("Universe", True, lambda player: False),
    ]
    + [
        Achievement(
            name=f"Scoring Achievement {n}",
            is_automatic=False,
            condition_met=partial(scoring_achievement_condition_met, level=n),
        )
        for n in range(1, 10)
    ]
)
