from abc import ABC
from dataclasses import dataclass
from frozendict import frozendict
from typing import List
from typing import Dict


@dataclass
class Registerable(ABC):
    name: str

    def __eq__(self, other):
        return isinstance(other, Registerable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class MutableRegistry:
    def __init__(self, registry: List[Registerable]):
        self._registry = {member.name: member for member in registry}

    @property
    def registry(self) -> Dict:
        return self._registry

    def to_immutable_registry(self):
        return ImmutableRegistry(list(self.registry.values()))


class ImmutableRegistry:
    def __init__(self, registry: List[Registerable]):
        self._registry = frozendict({member.name: member for member in registry})

    @property
    def registry(self) -> frozendict:
        return self._registry


def register_effect(
    registry: MutableRegistry = None, card_name: str = None, position: int = 0
):
    def decorator_register_effect(wrapped_class):
        card = registry.registry.get(card_name)
        effects = card.effects if card.effects else []
        new_effect = wrapped_class()

        if position < len(effects):
            effects[position] = new_effect
        else:
            effects.extend([None for _ in range(len(effects), position)])
            effects.append(new_effect)

        card.effects = effects

        return wrapped_class

    return decorator_register_effect
