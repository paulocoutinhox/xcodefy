from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(frozen=True, slots=True)
class GroupTreeAnchoredReference:
    anchor: GroupTreeReference
    relative_path: NamePath | None = None

    def encode(self, coder: Any) -> None:
        if self.relative_path is None:
            self.anchor.encode(coder)
            return
        container = coder.keyed()
        container.put_unconditionally("anchor", self.anchor)
        container.put_unconditionally("relative-path", self.relative_path)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is not ValueType.OBJECT:
            return cls(GroupTreeReference.decode(coder))
        container = coder.keyed()
        anchor = container.get("anchor", GroupTreeReference)
        relative_path = container.get("relative-path", NamePath)
        return cls(anchor, relative_path)

    def __str__(self) -> str:
        if self.relative_path is None:
            return str(self.anchor)
        return f"{self.anchor}/{self.relative_path}"
