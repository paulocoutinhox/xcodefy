from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.decoding_container import DecodingContainer
from xcodefy.library.serialization.values.value import Value


def test_a_container_captures_the_coder_path_and_value():
    coder = Decoder(Value.integer(1))
    container = DecodingContainer(coder)
    assert container.value == Value.integer(1)
    assert str(container.path) == ""
    assert container.coder is coder
