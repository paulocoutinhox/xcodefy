from xcodefy.errors.validation_error import ValidationError
from xcodefy.errors.xcodefy_error import XcodefyError


def test_a_validation_error_is_an_xcodefy_error():
    assert issubclass(ValidationError, XcodefyError)
    assert str(ValidationError("invalid")) == "invalid"
