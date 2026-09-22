import pytest

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.values.value import Value


def container():
    return Encoder().primitive()


@pytest.mark.parametrize(("method", "argument", "expected"), [("put_null", None, Value.null()), ("put_boolean", True, Value.boolean(True)), ("put_integer", 2, Value.integer(2)), ("put_double", 1.5, Value.double(1.5)), ("put_string", "a", Value.string("a"))])
def test_each_primitive_is_recorded_and_finished(method, argument, expected):
    opened = container()
    getattr(opened, method)() if argument is None else getattr(opened, method)(argument)
    assert opened.finish() == expected


def test_encoding_twice_is_rejected():
    opened = container()
    opened.put_integer(1)
    with pytest.raises(EncodeError, match="exactly one value"):
        opened.put_integer(2)


def test_finishing_without_a_value_is_rejected():
    with pytest.raises(EncodeError, match="without encoding a value"):
        container().finish()
