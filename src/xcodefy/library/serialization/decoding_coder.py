from typing import Any, Protocol

from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType


class DecodingCoder(Protocol):
    current: Value
    path: AbsolutePath

    def decode_child(self, value: Value, component: PathComponent, decode: Any) -> Any: ...

    def error_for_expected_type(self, expected: ValueType) -> Exception: ...
