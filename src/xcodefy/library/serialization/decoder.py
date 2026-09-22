from __future__ import annotations

from typing import Any

from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.xcodefy_error import XcodefyError
from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.keyed_decoding_container import KeyedDecodingContainer
from xcodefy.library.serialization.ordinal_decoding_container import OrdinalDecodingContainer
from xcodefy.library.serialization.parser import Parser
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.primitive_decoding_container import PrimitiveDecodingContainer
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType

SOURCE_ENCODING = "utf-8-sig"


class Decoder:
    def __init__(self, root: Value, tool_name: str = "Xcode") -> None:
        self.current = root
        self.path = AbsolutePath()
        self.tool_name = tool_name

    @property
    def current_node_type(self) -> ValueType:
        return self.current.type

    def primitive(self) -> PrimitiveDecodingContainer:
        return PrimitiveDecodingContainer(self)

    def ordinal(self) -> OrdinalDecodingContainer:
        return OrdinalDecodingContainer(self)

    def keyed(self) -> KeyedDecodingContainer:
        return KeyedDecodingContainer(self)

    def error_for_expected_type(self, expected: ValueType) -> DecodeError:
        return DecodeError(f"Expected an instance of {expected.error_message_name} but an instance of {self.current.type.error_message_name} was specified.")

    def decode_string(self) -> str:
        return self.primitive().string()

    def decode_boolean(self) -> bool:
        return self.primitive().boolean()

    def decode_integer(self) -> int:
        return self.primitive().integer()

    def decode_double(self) -> float:
        return self.primitive().double()

    def decode_child(self, value: Value, component: PathComponent, decode: Any) -> Any:
        previous_value = self.current
        previous_path = self.path
        self.current = value
        self.path = previous_path.appending_component(component)
        try:
            return Decoder.resolve(decode)(self)
        except DecodeError as error:
            if error.coding_path is not None:
                raise
            raise DecodeError(str(error), str(self.path)) from error
        except XcodefyError as error:
            raise DecodeError(str(error), str(self.path)) from error
        finally:
            self.current = previous_value
            self.path = previous_path

    @staticmethod
    def resolve(decode: Any) -> Any:
        return decode.decode if hasattr(decode, "decode") else decode

    @staticmethod
    def decode_value(value: Value, decode: Any) -> Any:
        coder = Decoder(value)
        try:
            return Decoder.resolve(decode)(coder)
        except DecodeError:
            raise
        except XcodefyError as error:
            raise DecodeError(str(error)) from error

    @staticmethod
    def decode_text(text: str | bytes, decode: Any) -> Any:
        return Decoder.decode_value(Parser(Decoder.decoded_source(text)).parse(), decode)

    @staticmethod
    def decoded_source(text: str | bytes) -> str:
        if isinstance(text, str):
            return text
        try:
            return text.decode(SOURCE_ENCODING)
        except UnicodeDecodeError as error:
            raise DecodeError("The document is not valid UTF-8 text.") from error
