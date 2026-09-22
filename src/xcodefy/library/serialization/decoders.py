from typing import Any

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.decoder import Decoder


class Decoders:
    @staticmethod
    def boolean(coder: Decoder) -> bool:
        return coder.decode_boolean()

    @staticmethod
    def integer(coder: Decoder) -> int:
        return coder.decode_integer()

    @staticmethod
    def double(coder: Decoder) -> float:
        return coder.decode_double()

    @staticmethod
    def string(coder: Decoder) -> str:
        return coder.decode_string()

    @staticmethod
    def array_of(decode: Any) -> Any:
        def decode_array(coder: Decoder) -> list[Any]:
            container = coder.ordinal()
            return [container.get(index, decode) for index in range(container.count)]

        return decode_array

    @staticmethod
    def set_of(decode: Any) -> Any:
        def decode_set(coder: Decoder) -> frozenset[Any]:
            container = coder.ordinal()
            elements = [container.get(index, decode) for index in range(container.count)]
            result = frozenset(elements)
            if len(result) != len(elements):
                raise DecodeError("Decoding a set produced duplicate elements.")
            return result

        return decode_set

    @staticmethod
    def dictionary_of(decode: Any) -> Any:
        def decode_dictionary(coder: Decoder) -> dict[str, Any]:
            container = coder.keyed()
            return {key: container.get(key, decode) for key in container.keys}

        return decode_dictionary

    @staticmethod
    def keyed_dictionary_of(key_type: Any, decode: Any) -> Any:
        def decode_keyed_dictionary(coder: Decoder) -> dict[Any, Any]:
            container = coder.keyed()
            return {key_type.from_encodable_string(key): container.get(key, decode) for key in container.keys}

        return decode_keyed_dictionary
