from src.innovation.utils.registry import Registerable
from dataclasses import dataclass
from functools import partial
from typing import Callable, Union, Any


@dataclass
class Achievement(Registerable):
    name: str
    is_automatic: bool
    condition_met: Union[Callable[[Any], bool], partial]
