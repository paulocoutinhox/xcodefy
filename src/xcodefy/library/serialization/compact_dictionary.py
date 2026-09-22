from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CompactDictionary:
    values: Mapping[Any, Any] = field(default_factory=dict)

    @classmethod
    def of(cls, values: Mapping[Any, Any]) -> CompactDictionary:
        return cls(values)
