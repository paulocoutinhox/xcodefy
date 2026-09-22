from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.values.group_tree_anchored_reference import GroupTreeAnchoredReference
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.name_path import NamePath

ANCHOR = GroupTreeReference.of_child_names(["Config"])


def test_an_anchor_without_a_relative_path_encodes_as_the_anchor_alone():
    assert RoundTrip.text(GroupTreeAnchoredReference(ANCHOR)) == '"Config"\n'


def test_an_anchor_with_a_relative_path_encodes_as_an_object():
    reference = GroupTreeAnchoredReference(ANCHOR, NamePath.of_child_names(["Debug.xcconfig"]))
    assert RoundTrip.text(reference) == '{\n  "anchor": "Config",\n  "relative-path": "Debug.xcconfig",\n}\n'


def test_a_reference_renders_for_diagnostics():
    assert str(GroupTreeAnchoredReference(ANCHOR)) == "Config"
    assert str(GroupTreeAnchoredReference(ANCHOR, NamePath.of_child_names(["a"]))) == "Config/a"
