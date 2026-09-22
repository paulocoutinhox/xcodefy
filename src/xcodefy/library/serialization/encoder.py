from __future__ import annotations

from typing import Any

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.coding_order import CodingOrder
from xcodefy.library.serialization.compact_array import CompactArray
from xcodefy.library.serialization.compact_dictionary import CompactDictionary
from xcodefy.library.serialization.encoding_container import EncodingContainer
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.keyed_encoding_container import KeyedEncodingContainer
from xcodefy.library.serialization.ordinal_encoding_container import OrdinalEncodingContainer
from xcodefy.library.serialization.primitive_encoding_container import PrimitiveEncodingContainer
from xcodefy.library.serialization.printer import Printer
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value


class Encoder:
    def __init__(self) -> None:
        self.current: EncodingContainer | None = None
        self.densities: dict[AbsolutePath, PrintingDensity] = {}

    def open(self, container_type: type, density: PrintingDensity | None) -> Any:
        component = self.current.component_being_encoded if self.current is not None else None
        container = container_type(self, self.current, component)
        self.current = container
        if density is not None:
            self.densities[container.path] = density
        return container

    def primitive(self) -> PrimitiveEncodingContainer:
        return self.open(PrimitiveEncodingContainer, None)

    def ordinal(self, density: PrintingDensity | None = None) -> OrdinalEncodingContainer:
        return self.open(OrdinalEncodingContainer, density)

    def keyed(self, density: PrintingDensity | None = None) -> KeyedEncodingContainer:
        return self.open(KeyedEncodingContainer, density)

    def note_density(self, path: AbsolutePath, density: PrintingDensity) -> None:
        self.densities[path] = density

    def encode_string(self, value: str) -> None:
        self.primitive().put_string(value)

    def encode_boolean(self, value: bool) -> None:
        self.primitive().put_boolean(value)

    def encode_integer(self, value: int) -> None:
        self.primitive().put_integer(value)

    def encode_double(self, value: float) -> None:
        self.primitive().put_double(value)

    def encode_child(self, value: Any) -> Value:
        original = self.current
        self._dispatch(value)
        if self.current is original:
            return Value.object([])
        opened = self.current
        if opened.parent is not original:
            raise EncodeError("An encoder opened more than one container for a single value.")
        self.current = original
        return opened.finish()

    def _dispatch(self, value: Any) -> None:
        if value is None:
            self.primitive().put_null()
        elif isinstance(value, bool):
            self.primitive().put_boolean(value)
        elif isinstance(value, int):
            self.primitive().put_integer(value)
        elif isinstance(value, float):
            self.primitive().put_double(value)
        elif isinstance(value, str):
            self.primitive().put_string(str(value))
        elif isinstance(value, CompactArray):
            self._dispatch_compact_array(value)
        elif isinstance(value, CompactDictionary):
            self._dispatch_compact_dictionary(value)
        elif isinstance(value, list | tuple):
            self._dispatch_sequence(value)
        elif isinstance(value, set | frozenset):
            self._dispatch_sequence(sorted(value, key=CodingOrder.key_string))
        elif isinstance(value, dict):
            self._dispatch_mapping(value, None)
        elif hasattr(value, "encode"):
            value.encode(self)
        else:
            raise EncodeError(f"A value of type {type(value).__name__} cannot be encoded.")

    def _dispatch_sequence(self, values: Any) -> None:
        container = self.ordinal()
        for element in values:
            container.put(element)

    def _dispatch_compact_array(self, value: CompactArray) -> None:
        container = self.ordinal()
        for element in value.values:
            container.put(element, PrintingDensity.COMPACT)

    def _dispatch_compact_dictionary(self, value: CompactDictionary) -> None:
        self._dispatch_mapping(value.values, PrintingDensity.COMPACT)

    def _dispatch_mapping(self, values: Any, density: PrintingDensity | None) -> None:
        container = self.keyed()
        for key in sorted(values, key=CodingOrder.key_string):
            container.put_unverified(CodingOrder.key_string(key), values[key], density)

    @staticmethod
    def json_for(value: Any) -> Value:
        return Encoder().encode_child(value)

    @staticmethod
    def data_for(value: Any, options: EncodingOptions) -> bytes:
        return Encoder.text_for(value, options).encode("utf-8")

    @staticmethod
    def text_for(value: Any, options: EncodingOptions) -> str:
        encoder = Encoder()
        root = encoder.encode_child(value)
        return Printer(options=options, densities=encoder.densities).print(root)
