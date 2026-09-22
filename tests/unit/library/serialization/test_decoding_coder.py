from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.decoding_coder import DecodingCoder
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType


def test_the_decoder_satisfies_every_call_the_containers_make():
    coder: DecodingCoder = Decoder(Value.integer(1))
    assert coder.current == Value.integer(1)
    assert str(coder.path) == ""
    assert coder.decode_child(Value.integer(2), PathComponent(key="a"), Decoders.integer) == 2
    assert isinstance(coder.error_for_expected_type(ValueType.STRING), Exception)
