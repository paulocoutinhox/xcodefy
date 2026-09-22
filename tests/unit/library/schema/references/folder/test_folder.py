from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.serialization.printing_density import PrintingDensity


def test_a_folder_without_exceptions_prints_compactly():
    folder = Folder()
    assert folder.printing_density is PrintingDensity.COMPACT
    folder.membership_exceptions.append(FolderExceptionSet.of_target(Instances.populated_target_exception_set()))
    assert folder.printing_density is None


def test_a_folder_is_only_printed_compactly_through_its_reference():
    assert RoundTrip.text(Folder()) == "{\n}\n"
    assert RoundTrip.text(Reference.of_folder(Folder())) == '{ "kind": "folder" }\n'


def test_the_discovery_overrides_are_written_when_present():
    text = RoundTrip.text(Instances.populated_folder())
    assert '"file-types"' in text
    assert '"opaque-folders"' in text
    assert '"target-membership"' in text


def test_a_populated_folder_round_trips():
    RoundTrip.expect_equal(Instances.populated_folder(), Folder)
