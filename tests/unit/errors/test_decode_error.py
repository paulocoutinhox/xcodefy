from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.xcodefy_error import XcodefyError


def test_a_decode_error_without_a_path_keeps_its_message():
    error = DecodeError("broken")
    assert issubclass(DecodeError, XcodefyError)
    assert str(error) == "broken"
    assert error.coding_path is None


def test_a_decode_error_with_a_path_appends_it():
    error = DecodeError("broken", "/files[0]")
    assert str(error) == "broken at /files[0]"
    assert error.message == "broken"
    assert error.coding_path == "/files[0]"


def test_an_empty_coding_path_is_treated_as_absent():
    error = DecodeError("broken", "")
    assert str(error) == "broken"
    assert error.coding_path is None
