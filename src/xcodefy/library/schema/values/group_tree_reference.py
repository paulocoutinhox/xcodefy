from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.values.value_type import ValueType
from xcodefy.library.utilities.text import Text

ID_SIGNALLING_PREFIX = "id:"


@dataclass(frozen=True, slots=True)
class GroupTreeReference:
    object_id: ObjectID | None = None
    name_path: NamePath | None = None

    def __post_init__(self) -> None:
        if (self.object_id is None) == (self.name_path is None):
            raise ValidationError("A group tree reference is either an object id or a name path.")

    @classmethod
    def of_object_id(cls, object_id: ObjectID) -> Self:
        return cls(object_id=object_id)

    @classmethod
    def of_name_path(cls, name_path: NamePath) -> Self:
        return cls(name_path=name_path)

    @classmethod
    def of_child_names(cls, names: Any) -> Self:
        return cls(name_path=NamePath.of_child_names(names))

    @property
    def string_encoding(self) -> str | None:
        if self.object_id is not None:
            return ID_SIGNALLING_PREFIX + self.object_id.encodable_string_representation
        representation = self.name_path.lossless_path_representation
        if representation is not None and not representation.startswith(ID_SIGNALLING_PREFIX):
            return representation
        return None

    @property
    def encodes_to_string(self) -> bool:
        return self.string_encoding is not None

    def encode(self, coder: Any) -> None:
        encoding = self.string_encoding
        if encoding is not None:
            coder.encode_string(encoding)
            return
        container = coder.ordinal()
        for component in self.name_path.components:
            container.put(component)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls._decode_string(coder.decode_string())
        return cls.of_name_path(NamePath.decode(coder))

    @classmethod
    def _decode_string(cls, value: str) -> Self:
        identifier = Text.dropping_required_prefix(value, ID_SIGNALLING_PREFIX)
        if identifier is not None:
            return cls.of_object_id(ObjectID(identifier))
        return cls.of_name_path(NamePath.from_lossless_path(value))

    def __str__(self) -> str:
        if self.object_id is not None:
            return ID_SIGNALLING_PREFIX + self.object_id.encodable_string_representation
        return str(self.name_path)
