from abc import ABC
from dataclasses import dataclass
from frozendict import frozendict
from typing import List


@dataclass(frozen=True)
class Registerable(ABC):
    name: str

    def __hash__(self):
        return hash(self.name)


class ImmutableRegistry:
    def __init__(self, registry: List[Registerable]):
        self._registry = frozendict({member.name: member for member in registry})

    @property
    def registry(self) -> frozendict:
        return self._registry
