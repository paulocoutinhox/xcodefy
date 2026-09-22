from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EncodingOptions:
    add_trailing_newline: bool = True

    @classmethod
    def default(cls) -> EncodingOptions:
        return cls()
