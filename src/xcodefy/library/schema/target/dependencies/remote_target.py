from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class RemoteTarget(InlineKeyedCodable):
    project: GroupTreeReference
    target: str
    target_id: ObjectID

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("project", self.project)
        container.put_unconditionally("target", self.target)
        container.put_unconditionally("target-id", self.target_id)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        project = container.get("project", GroupTreeReference)
        target = container.get("target", Decoders.string)
        return cls(project, target, container.get("target-id", ObjectID))
