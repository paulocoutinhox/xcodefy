from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_phases.build_phase_scope import BuildPhaseScope
from xcodefy.library.schema.build_phases.copy_files_build_phase_properties import CopyFilesBuildPhaseProperties
from xcodefy.library.schema.values.bundle_base_path import BundleBasePath


def test_the_defaults_encode_to_nothing():
    assert RoundTrip.text(CopyFilesBuildPhaseProperties()) == "{\n}\n"


def test_the_destination_settings_are_written_when_present():
    properties = CopyFilesBuildPhaseProperties(bundle_base_path=BundleBasePath.RESOURCES_DIR, relative_path="Sub", scope=BuildPhaseScope.INSTALL)
    assert RoundTrip.text(properties) == '{\n  "bundle-base-path": "resources-directory",\n  "relative-path": "Sub",\n  "scope": "install",\n}\n'


def test_the_phase_name_comes_from_the_base_properties():
    assert Instances.populated_copy_properties().name == "Copy Files"


def test_a_copy_phase_never_prints_compactly():
    assert CopyFilesBuildPhaseProperties().printing_density is None


def test_populated_properties_round_trip():
    RoundTrip.expect_equal(Instances.populated_copy_properties(), CopyFilesBuildPhaseProperties)
