import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.references.reference_kind import ReferenceKind


def test_a_file_reference_omits_the_default_kind():
    assert RoundTrip.text(Reference.of_file(FileReference())) == "{}\n"


@pytest.mark.parametrize("kind", [ReferenceKind.GROUP, ReferenceKind.FOLDER, ReferenceKind.VARIANT_GROUP, ReferenceKind.VERSION_GROUP])
def test_every_other_kind_is_written(kind):
    contents = {ReferenceKind.GROUP: Instances.populated_group(), ReferenceKind.FOLDER: Instances.populated_folder(), ReferenceKind.VARIANT_GROUP: Instances.populated_variant_group(), ReferenceKind.VERSION_GROUP: Instances.populated_version_group()}
    reference = Reference(kind, contents[kind])
    assert f'"kind": "{kind.value}"' in RoundTrip.text(reference)
    RoundTrip.expect_equal(reference, Reference)


def test_mismatched_content_is_rejected():
    with pytest.raises(ValidationError, match="requires Group"):
        Reference(ReferenceKind.GROUP, FileReference())


def test_the_printing_density_is_delegated_to_the_content():
    assert Reference.of_file(FileReference()).printing_density is not None
    assert Reference.of_group(Instances.populated_group()).printing_density is None


def test_nested_groups_round_trip():
    inner = Reference.of_group(Group(children=[Reference.of_file(FileReference())]))
    RoundTrip.expect_equal(Reference.of_group(Group(children=[inner])), Reference)
