from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True, order=False)
class LexicographicalOrder:
    content: tuple[Any, ...]

    def __lt__(self, other: LexicographicalOrder) -> bool:
        return self.content < other.content
