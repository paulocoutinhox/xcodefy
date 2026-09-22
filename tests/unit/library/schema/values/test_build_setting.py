import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.build_setting import BuildSetting


def test_a_setting_is_either_a_string_or_an_array():
    assert BuildSetting.of_string("a").string == "a"
    assert BuildSetting.of_array(["a"]).array == ("a",)


@pytest.mark.parametrize("arguments", [{}, {"string": "a", "array": ("b",)}])
def test_a_setting_rejects_carrying_neither_or_both(arguments):
    with pytest.raises(ValidationError, match="either a string or an array"):
        BuildSetting(**arguments)


def test_a_string_setting_encodes_as_a_bare_string():
    assert RoundTrip.text(BuildSetting.of_string("a")) == '"a"\n'


def test_an_array_setting_encodes_as_an_array():
    assert RoundTrip.text(BuildSetting.of_array(["a", "b"])) == '[\n  "a",\n  "b",\n]\n'


def test_an_empty_array_setting_round_trips():
    RoundTrip.expect_equal(BuildSetting.of_array([]), BuildSetting)


def test_a_string_setting_rejects_a_non_string():
    with pytest.raises(ValidationError, match="must hold a string"):
        BuildSetting.of_string(5)


def test_an_array_setting_rejects_a_non_string_element():
    with pytest.raises(ValidationError, match="must hold only strings"):
        BuildSetting.of_array(["a", 2])
