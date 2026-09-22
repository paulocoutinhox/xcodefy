import pytest

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.serialization.decoder import Decoder
from xcodefy.library.serialization.values.value import Value


def container(value):
    return Decoder(value).primitive()


def test_each_typed_accessor_returns_its_content():
    assert container(Value.boolean(True)).boolean() is True
    assert container(Value.integer(2)).integer() == 2
    assert container(Value.double(1.5)).double() == 1.5
    assert container(Value.string("a")).string() == "a"


@pytest.mark.parametrize("method", ["boolean", "integer", "double", "string"])
def test_a_mismatched_type_is_reported_with_both_type_names(method):
    with pytest.raises(DecodeError, match="Expected an instance of"):
        getattr(container(Value.array([])), method)()


def test_the_error_message_names_the_dictionary_type():
    with pytest.raises(DecodeError, match="but an instance of dictionary was specified"):
        container(Value.object([])).string()
