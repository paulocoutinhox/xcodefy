from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.relative_reference import RelativeReference


def test_a_path_is_built_from_child_names():
    assert NamePath.of_child_names(["a", "b"]) == NamePath((NamePathComponent.child("a"), NamePathComponent.child("b")))


def test_an_empty_path_has_no_lossless_representation():
    assert NamePath().lossless_path_representation is None


def test_a_clean_path_joins_with_slashes():
    assert NamePath.of_child_names(["a", "b"]).lossless_path_representation == "a/b"


def test_a_path_with_an_ambiguous_component_has_no_lossless_representation():
    assert NamePath((NamePathComponent.child(".."),)).lossless_path_representation is None


def test_an_empty_string_decodes_to_a_single_empty_child():
    assert NamePath.from_lossless_path("") == NamePath((NamePathComponent.child(""),))


def test_a_slash_separated_string_decodes_into_components():
    assert NamePath.from_lossless_path("../a") == NamePath((NamePathComponent.of_relative(RelativeReference.PARENT), NamePathComponent.child("a")))


def test_a_clean_path_encodes_as_a_bare_string():
    assert RoundTrip.text(NamePath.of_child_names(["a", "b"])) == '"a/b"\n'


def test_a_path_that_cannot_be_joined_encodes_as_an_array():
    assert RoundTrip.text(NamePath((NamePathComponent.child(".."),))) == '[\n  {\n    "name": "..",\n  },\n]\n'


def test_paths_concatenate():
    assert NamePath.of_child_names(["a"]) + NamePath.of_child_names(["b"]) == NamePath.of_child_names(["a", "b"])


def test_a_path_renders_for_diagnostics():
    assert str(NamePath.of_child_names(["a", "b"])) == "a/b"
