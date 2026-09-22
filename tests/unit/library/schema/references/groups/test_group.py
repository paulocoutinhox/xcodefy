from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.serialization.printing_density import PrintingDensity


def test_a_group_named_after_its_path_omits_the_name():
    group = Group.named_after_path(FilePath(FilePathBase.group(), "Sources"))
    assert group.name == "Sources"
    assert RoundTrip.text(Reference.of_group(group)) == '{ "kind": "group", "path": "Sources" }\n'


def test_a_group_with_a_distinct_name_writes_it():
    group = Group(FilePath(FilePathBase.group(), "Sources"), "Other")
    assert '"name": "Other"' in RoundTrip.text(Reference.of_group(group))


def test_a_childless_group_prints_compactly():
    group = Group.named_after_path(FilePath(FilePathBase.group(), "Sources"))
    assert group.printing_density is PrintingDensity.COMPACT
    group.children.append(Reference.of_file(Instances.populated_file_reference()))
    assert group.printing_density is None


def test_children_default_to_an_empty_list():
    assert Group.named_after_path(FilePath(FilePathBase.group(), "Sources")).children == []


def test_a_populated_group_round_trips_through_a_reference():
    RoundTrip.expect_equal(Reference.of_group(Instances.populated_group()), Reference)
