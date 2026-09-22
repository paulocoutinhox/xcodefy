from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class LocalSwiftPackage(InlineKeyedCodable):
    path: str = ""

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("path", self.path)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        return cls(container.get("path", Decoders.string))
