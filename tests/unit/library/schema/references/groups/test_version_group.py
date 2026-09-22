from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.serialization.printing_density import PrintingDensity


def test_a_childless_group_with_at_most_one_build_file_prints_compactly():
    group = VersionGroup()
    assert group.printing_density is PrintingDensity.COMPACT
    group.build_files.append(Instances.populated_project_build_file())
    assert group.printing_density is PrintingDensity.COMPACT
    group.build_files.append(Instances.populated_project_build_file())
    assert group.printing_density is None


def test_the_current_version_and_type_are_written_when_present():
    text = RoundTrip.text(Instances.populated_version_group())
    assert '"current-version"' in text
    assert '"type": "sourcecode.swift"' in text


def test_a_populated_group_round_trips():
    RoundTrip.expect_equal(Instances.populated_version_group(), VersionGroup)
