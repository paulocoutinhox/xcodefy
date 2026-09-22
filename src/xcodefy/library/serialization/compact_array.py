from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CompactArray:
    values: tuple[Any, ...] = ()

    @classmethod
    def of(cls, values: Iterable[Any]) -> CompactArray:
        return cls(tuple(values))
