from __future__ import annotations

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.encoding_coder import EncodingCoder
from xcodefy.library.serialization.encoding_container import EncodingContainer
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value


class PrimitiveEncodingContainer(EncodingContainer):
    def __init__(self, coder: EncodingCoder, parent: EncodingContainer | None, component: PathComponent | None) -> None:
        super().__init__(coder, parent, component)
        self.encoded: Value | None = None

    def put(self, value: Value) -> None:
        if self.encoded is not None:
            raise EncodeError("A primitive container encodes exactly one value.")
        self.encoded = value

    def put_null(self) -> None:
        self.put(Value.null())

    def put_boolean(self, value: bool) -> None:
        self.put(Value.boolean(value))

    def put_integer(self, value: int) -> None:
        self.put(Value.integer(value))

    def put_double(self, value: float) -> None:
        self.put(Value.double(value))

    def put_string(self, value: str) -> None:
        self.put(Value.string(value))

    def finish(self) -> Value:
        if self.encoded is None:
            raise EncodeError("A primitive container finished without encoding a value.")
        return self.encoded
