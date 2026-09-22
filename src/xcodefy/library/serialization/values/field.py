from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Field:
    key: str
    value: Any
