import pytest

from tests.support.combinatorics import Combinatorics
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.string_encoding import StringEncoding
from xcodefy.library.schema.values.text_encoding import TextEncoding

HARD_NAME_FRAGMENTS = ["", "/", "a", "b"]
HARD_VERSION_FRAGMENTS = [".", "..", "1", "<", "2"]
HARD_PATH_FRAGMENTS = ["$", "(", ")", "a"]
RELATIVE_BASES = [FilePathBase.group(), FilePathBase.project(), FilePathBase.developer(), FilePathBase.build_products(), FilePathBase.sdk()]


@pytest.mark.parametrize("encoding", list(StringEncoding))
def test_every_named_text_encoding_round_trips(encoding):
    RoundTrip.expect_equal(TextEncoding.of(encoding), TextEncoding)


def test_an_unknown_text_encoding_is_persisted_as_its_integer_value():
    RoundTrip.expect_equal(TextEncoding(23418341), TextEncoding)
    assert RoundTrip.text(TextEncoding(23418341)) == "23418341\n"


def test_a_target_build_phase_reference_without_a_name_round_trips():
    RoundTrip.expect_equal(TargetBuildPhaseReference.named(BuildPhaseKind.COPY), TargetBuildPhaseReference)


@pytest.mark.parametrize("name", Combinatorics.subset_permutation_joinings(HARD_NAME_FRAGMENTS))
def test_target_build_phase_names_survive_escaping(name):
    RoundTrip.expect_equal(TargetBuildPhaseReference.named(BuildPhaseKind.COPY, name), TargetBuildPhaseReference)


@pytest.mark.parametrize("target_name", Combinatorics.subset_permutation_joinings(HARD_NAME_FRAGMENTS))
def test_project_build_phase_targets_survive_escaping(target_name):
    reference = ProjectBuildPhaseReference.named(LocalTargetReference(target_name), BuildPhaseKind.COPY)
    RoundTrip.expect_equal(reference, ProjectBuildPhaseReference)


@pytest.mark.parametrize("phase_name", Combinatorics.subset_permutation_joinings(HARD_NAME_FRAGMENTS))
def test_project_build_phase_names_survive_escaping(phase_name):
    reference = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.COPY, phase_name)
    RoundTrip.expect_equal(reference, ProjectBuildPhaseReference)


@pytest.mark.parametrize("fragment", Combinatorics.subset_permutation_joinings(HARD_VERSION_FRAGMENTS))
def test_swift_package_version_constraints_survive_escaping(fragment):
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.revision(fragment), SwiftPackageVersionConstraint)
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.branch(fragment), SwiftPackageVersionConstraint)
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.version(fragment), SwiftPackageVersionConstraint)
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.version_range(fragment, fragment), SwiftPackageVersionConstraint)
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.up_to_next_minor_version(fragment), SwiftPackageVersionConstraint)
    RoundTrip.expect_equal(SwiftPackageVersionConstraint.up_to_next_major_version(fragment), SwiftPackageVersionConstraint)


@pytest.mark.parametrize("build_setting", ["PRODUCTS", "", "$", "$a", "$()", "$asdf", "$(asdf)"])
def test_source_root_file_paths_survive_escaping(build_setting):
    RoundTrip.expect_equal(FilePath(FilePathBase.source_root(build_setting), ""), FilePath)


@pytest.mark.parametrize("path", ["", ".", "..", "./"])
def test_project_relative_file_paths_survive_escaping(path):
    RoundTrip.expect_equal(FilePath(FilePathBase.project(), path), FilePath)


@pytest.mark.parametrize("path", ["/", "/.", "/.."])
def test_absolute_file_paths_survive_escaping(path):
    RoundTrip.expect_equal(FilePath(FilePathBase.absolute(), path), FilePath)


@pytest.mark.parametrize("path", Combinatorics.subset_permutation_joinings(HARD_PATH_FRAGMENTS))
def test_group_relative_file_paths_survive_escaping(path):
    RoundTrip.expect_equal(FilePath(FilePathBase.group(), path), FilePath)


@pytest.mark.parametrize("base", RELATIVE_BASES, ids=lambda base: base.kind.value)
def test_every_relative_base_survives_escaping(base):
    for path in Combinatorics.subset_permutation_joinings(["A", "B", "<", ">", "USER", "\\"]):
        if not path.startswith("/"):
            RoundTrip.expect_equal(FilePath(base, path), FilePath)


@pytest.mark.parametrize("name", Combinatorics.subset_permutation_joinings(["a", "", "/", "//", ".", ".."]))
def test_name_path_children_survive_escaping(name):
    RoundTrip.expect_equal(NamePath((NamePathComponent.child(name),)), NamePath)
