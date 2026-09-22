from xcodefy.library.serialization.encoding_options import EncodingOptions


def test_the_default_options_add_a_trailing_newline():
    assert EncodingOptions.default() == EncodingOptions()
    assert EncodingOptions.default().add_trailing_newline is True


def test_the_trailing_newline_can_be_disabled():
    assert EncodingOptions(add_trailing_newline=False).add_trailing_newline is False
