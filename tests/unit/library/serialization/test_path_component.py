import pytest

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.path_component import PathComponent


def test_a_component_renders_as_a_key_or_an_index():
    assert str(PathComponent(key="files")) == "/files"
    assert str(PathComponent(index=2)) == "[2]"


@pytest.mark.parametrize("arguments", [{}, {"key": "a", "index": 1}])
def test_a_component_requires_exactly_one_locator(arguments):
    with pytest.raises(ValidationError, match="exactly one locator"):
        PathComponent(**arguments)
