from typing import Any

from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions


class RoundTrip:
    @staticmethod
    def text(value: Any) -> str:
        return Encoder.text_for(value, EncodingOptions.default())

    @staticmethod
    def decode(text: str, decode: Any) -> Any:
        return Decoder.decode_text(text, decode)

    @staticmethod
    def expect_equal(value: Any, decode: Any) -> None:
        text = RoundTrip.text(value)
        decoded = RoundTrip.decode(text, decode)
        assert decoded == value, f"{decoded!r} != {value!r} via {text!r}"
