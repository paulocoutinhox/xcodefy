from xcodefy.errors.xcodefy_error import XcodefyError


def test_the_base_error_is_an_exception_carrying_its_message():
    error = XcodefyError("broken")
    assert isinstance(error, Exception)
    assert str(error) == "broken"
