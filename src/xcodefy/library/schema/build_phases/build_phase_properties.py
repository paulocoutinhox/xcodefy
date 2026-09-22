from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class BuildPhaseProperties(InlineKeyedCodable):
    object_id: ObjectID | None = None
    name: str | None = None

    @property
    def everything_is_default(self) -> bool:
        return self == BuildPhaseProperties()

    @property
    def printing_density(self) -> PrintingDensity | None:
        return PrintingDensity.COMPACT

    def encode_inline(self, container: Any) -> None:
        container.put("id", self.object_id, None)
        container.put("name", self.name, None)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        object_id = container.get_optional("id", ObjectID)
        name = container.get_optional("name", Decoders.string)
        return cls(object_id, name)
