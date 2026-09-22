from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.object import Object
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment
from xcodefy.library.serialization.values.value_type import ValueType

SCALAR_TYPES = frozenset({ValueType.NULL, ValueType.BOOLEAN, ValueType.INTEGER, ValueType.DOUBLE, ValueType.STRING})


@dataclass(slots=True)
class Value:
    type: ValueType
    content: Any = None

    @classmethod
    def null(cls) -> Value:
        return cls(ValueType.NULL)

    @classmethod
    def boolean(cls, content: bool) -> Value:
        return cls(ValueType.BOOLEAN, content)

    @classmethod
    def integer(cls, content: int) -> Value:
        return cls(ValueType.INTEGER, content)

    @classmethod
    def double(cls, content: float) -> Value:
        return cls(ValueType.DOUBLE, content)

    @classmethod
    def string(cls, content: str) -> Value:
        return cls(ValueType.STRING, content)

    @classmethod
    def array(cls, content: list[ValueOrComment]) -> Value:
        return cls(ValueType.ARRAY, content)

    @classmethod
    def object(cls, content: Object | list[FieldOrComment]) -> Value:
        return cls(ValueType.OBJECT, content if isinstance(content, Object) else Object(content))

    @property
    def is_container(self) -> bool:
        return self.type not in SCALAR_TYPES

    @classmethod
    def from_python(cls, value: Any) -> Value:
        if value is None:
            return cls.null()
        if isinstance(value, bool):
            return cls.boolean(value)
        if isinstance(value, int):
            return cls.integer(value)
        if isinstance(value, float):
            return cls.double(value)
        if isinstance(value, str):
            return cls.string(value)
        if isinstance(value, list | tuple):
            return cls.array([ValueOrComment(value=cls.from_python(item)) for item in value])
        if isinstance(value, dict) and all(isinstance(key, str) for key in value):
            return cls.object([FieldOrComment(field=Field(key, cls.from_python(item))) for key, item in value.items()])
        raise EncodeError(f"Unsupported JSON value type: {type(value).__name__}.")

    def to_python(self) -> Any:
        if self.type is ValueType.NULL:
            return None
        if self.type in SCALAR_TYPES:
            return self.content
        if self.type is ValueType.ARRAY:
            return [entry.value.to_python() for entry in self.content if entry.is_value]
        return {entry.field.key: entry.field.value.to_python() for entry in self.content.fields_or_comments if entry.is_field}
