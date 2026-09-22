from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.printing_density import PrintingDensity


@dataclass(slots=True)
class Group:
    path: FilePath = field(default_factory=FilePath)
    name: str = ""
    object_id: ObjectID | None = None
    common_properties: CommonReferenceProperties = field(default_factory=CommonReferenceProperties)
    children: list[Any] = field(default_factory=list)

    @classmethod
    def named_after_path(cls, path: FilePath, children: Any = None, object_id: ObjectID | None = None) -> Self:
        return cls(path, path.name, object_id, CommonReferenceProperties(), list(children or []))

    @property
    def printing_density(self) -> PrintingDensity | None:
        return PrintingDensity.COMPACT if not self.children else None

    def encode_inline(self, container: Any) -> None:
        container.put("id", self.object_id, None)
        container.put_inline(self.path)
        container.put("name", self.name, self.path.name)
        container.put_inline(self.common_properties)
        container.put("children", self.children, [])

    @classmethod
    def decode_inline(cls, container: Any, child_type: Any) -> Self:
        object_id = container.get_optional("id", ObjectID)
        path = container.get_inline(FilePath)
        name = container.get_or_default("name", Decoders.string, path.name)
        common_properties = container.get_inline(CommonReferenceProperties)
        children = container.get_or_default("children", Decoders.array_of(child_type), [])
        return cls(path, name, object_id, common_properties, children)
