from typing import Any

from xcodefy.errors.encode_error import EncodeError


class CodingOrder:
    @staticmethod
    def key_string(value: Any) -> str:
        if isinstance(value, str):
            return value
        representation = getattr(value, "encodable_string_representation", None)
        if isinstance(representation, str):
            return representation
        raise EncodeError(f"A {type(value).__name__} key cannot be encoded as a string.")
