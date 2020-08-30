from src.innovation.cards.achievement_registry import (
    GLOBAL_ACHIEVEMENTS_REGISTRY,
    scoring_achievement_condition_met,
)
import pytest
from mock import Mock


@pytest.mark.parametrize(
    "score, max_age_top_card, achievement_level, should_achieve",
    [
        (0, 1, 1, False),
        (4, 1, 1, False),
        (5, 1, 1, True),
        (6, 1, 1, True),
        (10, 1, 2, False),
        (10, 2, 2, True),
        (10, 3, 2, True),
        (34, 7, 6, True),
        (44, 9, 9, False),
        (49, 8, 9, False),
        (45, 9, 9, True),
    ],
)
def test_scoring_achievement(
    score, max_age_top_card, achievement_level, should_achieve
):
    player = Mock()
    player.score = score
    player.max_age_top_card = max_age_top_card

    assert (
        scoring_achievement_condition_met(player, achievement_level) == should_achieve
    )

    scoring_achievement = GLOBAL_ACHIEVEMENTS_REGISTRY.registry.get(
        f"Scoring Achievement {achievement_level}"
    )
    assert scoring_achievement.condition_met(player) == should_achieve
