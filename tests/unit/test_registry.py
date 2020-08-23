from src.innovation.cards.achievements import GLOBAL_ACHIEVEMENTS_REGISTRY
from src.innovation.cards.cards import GLOBAL_CARD_REGISTRY


def test_card_registry_names():
    cards = GLOBAL_CARD_REGISTRY.registry
    for card_name, card in cards.items():
        assert card_name == card.name


def test_card_registry_symbols():
    cards = GLOBAL_CARD_REGISTRY.registry
    for card in cards.values():
        symbols = card.symbols
        assert len(symbols) == 3
        assert len({symbol.position for symbol in symbols}) == 3


def test_achievement_registry_contents():
    achievements = GLOBAL_ACHIEVEMENTS_REGISTRY.registry.values()
    assert len(achievements) == 14
    assert sum(1 for a in achievements if a.is_automatic) == 5  # Non-scoring achievements
    assert sum(1 for a in achievements if not a.is_automatic) == 9  # Scoring achievements
    assert all(card_name == card.name for card_name, card in GLOBAL_ACHIEVEMENTS_REGISTRY.registry.items())

    expected_scoring_achievements = {
        f"Scoring Achievement {n}" for n in range(1, 10)
    }

    expected_non_scoring_achievements = {
        "Monument",
        "Empire",
        "Wonder",
        "World",
        "Universe"
    }

    assert all(
        a in GLOBAL_ACHIEVEMENTS_REGISTRY.registry for a in
        expected_scoring_achievements & expected_non_scoring_achievements
    )
