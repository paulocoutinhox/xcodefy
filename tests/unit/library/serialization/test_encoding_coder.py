from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_coder import EncodingCoder
from xcodefy.library.serialization.keyed_encoding_container import KeyedEncodingContainer
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value


def test_the_encoder_satisfies_every_call_the_containers_make():
    coder: EncodingCoder = Encoder()
    container = coder.open(KeyedEncodingContainer, PrintingDensity.COMPACT)
    assert coder.encode_child("a") == Value.string("a")
    coder.note_density(container.path.appending_key("k"), PrintingDensity.COMPACT)
    assert coder.densities[container.path.appending_key("k")] is PrintingDensity.COMPACT


def test_opening_a_container_records_the_requested_density():
    encoder = Encoder()
    container = encoder.open(KeyedEncodingContainer, PrintingDensity.COMPACT)
    assert encoder.densities[container.path] is PrintingDensity.COMPACT
    assert encoder.current is container
