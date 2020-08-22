from src.innovation.cards import GLOBAL_CARD_REGISTRY


def test_card_registry_names():
    cards = GLOBAL_CARD_REGISTRY.cards
    for card_name, card in cards.items():
        assert card_name == card.name


def test_card_registry_symbols():
    cards = GLOBAL_CARD_REGISTRY.cards
    for card in cards.values():
        symbols = card.symbols
        assert len(symbols) == 3
        assert len({symbol.position for symbol in symbols}) == 3
