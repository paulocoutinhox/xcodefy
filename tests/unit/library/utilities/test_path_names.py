import pytest

from xcodefy.library.utilities.path_names import PathNames


@pytest.mark.parametrize(("path", "components"), [("", []), ("a", ["a"]), ("a/b", ["a", "b"]), ("/a/b", ["/", "a", "b"]), ("a//b", ["a", "b"])])
def test_path_components_match_the_foundation_behaviour(path, components):
    assert PathNames.path_components(path) == components


@pytest.mark.parametrize(("path", "name"), [("", ""), ("a", "a"), ("/a/b.swift", "b.swift"), ("/", "/")])
def test_last_path_component_returns_the_trailing_name(path, name):
    assert PathNames.last_path_component(path) == name


def test_expanding_a_tilde_produces_an_absolute_path():
    assert not PathNames.expanding_tilde("~/Demo").startswith("~")
    assert PathNames.expanding_tilde("Demo") == "Demo"
