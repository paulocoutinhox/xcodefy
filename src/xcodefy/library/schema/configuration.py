from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.group_tree_anchored_reference import GroupTreeAnchoredReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(slots=True)
class Configuration:
    name: ConfigurationName
    file: GroupTreeAnchoredReference | None = None
    object_id: ObjectID | None = None

    @property
    def is_specialized(self) -> bool:
        return self.file is not None or self.object_id is not None

    def encode(self, coder: Any) -> None:
        if not self.is_specialized:
            coder.encode_string(self.name.raw_value)
            return
        container = coder.keyed()
        container.put("id", self.object_id, None)
        container.put_unconditionally("name", self.name)
        container.put("file", self.file, None, PrintingDensity.COMPACT)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls(ConfigurationName(coder.decode_string()))
        container = coder.keyed()
        object_id = container.get_optional("id", ObjectID)
        name = container.get("name", ConfigurationName)
        return cls(name, container.get_optional("file", GroupTreeAnchoredReference), object_id)
