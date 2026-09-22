from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(frozen=True, slots=True)
class CommonReferenceProperties(InlineKeyedCodable):
    include_in_index: bool | None = None

    def encode_inline(self, container: Any) -> None:
        container.put("index", self.include_in_index, None)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        return cls(container.get_optional("index", Decoders.boolean))
