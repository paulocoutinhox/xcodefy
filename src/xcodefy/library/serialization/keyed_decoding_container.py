from typing import Any

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.decoding_coder import DecodingCoder
from xcodefy.library.serialization.decoding_container import DecodingContainer
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType
from xcodefy.library.utilities.text import Text

MISSING = object()


class KeyedDecodingContainer(DecodingContainer):
    def __init__(self, coder: DecodingCoder) -> None:
        super().__init__(coder)
        if self.value.type is not ValueType.OBJECT:
            raise coder.error_for_expected_type(ValueType.OBJECT)
        self.fields: dict[str, Value] = {entry.field.key: entry.field.value for entry in self.value.content.fields_or_comments if entry.is_field}

    @property
    def count(self) -> int:
        return len(self.fields)

    @property
    def keys(self) -> list[str]:
        return list(self.fields)

    def contains(self, key: str) -> bool:
        return key in self.fields

    def _decode(self, key: str, decode: Any) -> Any:
        return self.coder.decode_child(self.fields[key], PathComponent(key=key), decode)

    def get(self, key: str, decode: Any) -> Any:
        if key not in self.fields:
            raise DecodeError(f"Missing required value for key {Text.smart_quoted(key)} at {Text.smart_quoted(str(self.path))}.")
        return self._decode(key, decode)

    def get_or_default(self, key: str, decode: Any, default: Any) -> Any:
        return self._decode(key, decode) if key in self.fields else default

    def get_optional(self, key: str, decode: Any) -> Any:
        return self.get_optional_with_default(key, decode, None)

    def get_optional_with_default(self, key: str, decode: Any, default: Any) -> Any:
        if key not in self.fields:
            return default
        return None if self.fields[key].type is ValueType.NULL else self._decode(key, decode)

    def get_if_present(self, key: str, decode: Any) -> Any:
        return self._decode(key, decode) if key in self.fields else None

    def get_inline(self, decode: Any) -> Any:
        return decode.decode_inline(self)
