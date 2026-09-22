from typing import Any

from xcodefy.library.serialization.decoding_container import DecodingContainer
from xcodefy.library.serialization.values.value_type import ValueType


class PrimitiveDecodingContainer(DecodingContainer):
    def _content(self, expected: ValueType) -> Any:
        if self.value.type is not expected:
            raise self.coder.error_for_expected_type(expected)
        return self.value.content

    def boolean(self) -> bool:
        return self._content(ValueType.BOOLEAN)

    def integer(self) -> int:
        return self._content(ValueType.INTEGER)

    def double(self) -> float:
        return self._content(ValueType.DOUBLE)

    def string(self) -> str:
        return self._content(ValueType.STRING)
