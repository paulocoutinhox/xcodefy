from xcodefy.errors.argument_error import ArgumentError
from xcodefy.errors.xcodefy_error import XcodefyError


def test_an_argument_error_is_an_xcodefy_error():
    assert issubclass(ArgumentError, XcodefyError)
    assert str(ArgumentError("bad flag")) == "bad flag"
