from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.inline_keyed_codable import InlineKeyedCodable


@dataclass(slots=True)
class Sample(InlineKeyedCodable):
    name: str = ""

    def encode_inline(self, container: Any) -> None:
        container.put_unconditionally("name", self.name)

    @classmethod
    def decode_inline(cls, container: Any) -> Self:
        return cls(container.get("name", lambda coder: coder.decode_string()))


def test_the_mixin_wraps_the_inline_form_in_a_keyed_container():
    encoded = Encoder.json_for(Sample("a"))
    assert encoded.to_python() == {"name": "a"}
    assert Decoder.decode_value(encoded, Sample) == Sample("a")
