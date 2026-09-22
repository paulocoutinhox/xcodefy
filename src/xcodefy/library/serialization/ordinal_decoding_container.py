from typing import Any

from xcodefy.library.serialization.decoding_coder import DecodingCoder
from xcodefy.library.serialization.decoding_container import DecodingContainer
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType


class OrdinalDecodingContainer(DecodingContainer):
    def __init__(self, coder: DecodingCoder) -> None:
        super().__init__(coder)
        if self.value.type is not ValueType.ARRAY:
            raise coder.error_for_expected_type(ValueType.ARRAY)
        self.elements: list[Value] = [entry.value for entry in self.value.content if entry.is_value]

    @property
    def count(self) -> int:
        return len(self.elements)

    def get(self, index: int, decode: Any) -> Any:
        return self.coder.decode_child(self.elements[index], PathComponent(index=index), decode)
