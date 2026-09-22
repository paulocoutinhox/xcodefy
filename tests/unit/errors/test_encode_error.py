from xcodefy.errors.encode_error import EncodeError
from xcodefy.errors.xcodefy_error import XcodefyError


def test_an_encode_error_is_an_xcodefy_error():
    assert issubclass(EncodeError, XcodefyError)
    assert str(EncodeError("cannot encode")) == "cannot encode"
