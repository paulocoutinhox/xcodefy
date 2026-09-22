import pytest

from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.object_id import ObjectID


def test_a_reference_is_either_an_object_id_or_a_name_path():
    assert GroupTreeReference.of_object_id(ObjectID("A1")).object_id == ObjectID("A1")
    assert GroupTreeReference.of_child_names(["a"]).name_path == NamePath.of_child_names(["a"])


@pytest.mark.parametrize("arguments", [{}, {"object_id": ObjectID("A1"), "name_path": NamePath()}])
def test_a_reference_rejects_carrying_neither_or_both(arguments):
    with pytest.raises(ValidationError, match="either an object id or a name path"):
        GroupTreeReference(**arguments)


def test_an_object_id_encodes_with_the_signalling_prefix():
    assert RoundTrip.text(GroupTreeReference.of_object_id(ObjectID("A1"))) == '"id:A1"\n'


def test_a_clean_name_path_encodes_as_a_bare_string():
    assert RoundTrip.text(GroupTreeReference.of_child_names(["a", "b"])) == '"a/b"\n'


def test_a_name_path_that_looks_like_an_object_id_falls_back_to_components():
    reference = GroupTreeReference.of_child_names(["id:a"])
    assert reference.encodes_to_string is False
    RoundTrip.expect_equal(reference, GroupTreeReference)


def test_a_name_path_with_an_ambiguous_component_falls_back_to_components():
    reference = GroupTreeReference.of_name_path(NamePath((NamePathComponent.child(".."),)))
    assert reference.encodes_to_string is False


def test_a_reference_renders_for_diagnostics():
    assert str(GroupTreeReference.of_object_id(ObjectID("A1"))) == "id:A1"
    assert str(GroupTreeReference.of_child_names(["a"])) == "a"
