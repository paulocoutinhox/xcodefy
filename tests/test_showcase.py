import pytest

from tests.support.showcase import PLATFORMS, PRODUCT_TYPES, SWIFT_SOURCES, Showcase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.references.reference_kind import ReferenceKind
from xcodefy.library.schema.target.dependencies.target_dependency_kind import TargetDependencyKind
from xcodefy.library.schema.target.target_kind import TargetKind
from xcodefy.tool.main import main
from xcodefy.xcode_project import XcodeProject


@pytest.fixture(scope="module")
def written(tmp_path_factory):
    directory = tmp_path_factory.mktemp("showcase")
    Showcase.write(directory)
    return directory


def joined(prefix, path):
    return "/".join(part for part in (prefix, path) if part)


def resolved_paths(project):
    found = []

    def walk(references, prefix):
        for reference in references:
            location = joined(prefix, reference.content.path.path)
            if reference.kind is ReferenceKind.GROUP:
                walk(reference.content.children, location)
            elif reference.kind in {ReferenceKind.FILE_REFERENCE, ReferenceKind.FOLDER}:
                found.append(location)
            else:
                found.extend(joined(location, child.path.path) for child in reference.content.children)

    walk(project.top_level_references, "")
    return found


def test_every_product_type_is_represented(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    produced = {target.common_properties.product_type_id.abbreviated_representation for target in project.targets if target.common_properties.product_type_id is not None}
    assert produced == {product_type for product_type, _ in PRODUCT_TYPES.values()}


def test_every_platform_is_represented(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    produced = {target.build_settings["SDKROOT"].string for target in project.targets if "SDKROOT" in target.build_settings}
    assert produced == set(PLATFORMS)


def test_every_target_kind_is_represented(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    assert {target.kind for target in project.targets} == set(TargetKind)


def test_every_build_phase_kind_is_represented(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    produced = {phase.kind for target in project.targets for phase in target.common_properties.build_phases}
    assert produced == set(BuildPhaseKind)


def test_every_reference_kind_is_represented(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    assert {reference.kind for reference in project.references()} == set(ReferenceKind)


def test_every_referenced_path_exists_on_disk(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    missing = [path for path in resolved_paths(project) if not (written / path).exists()]
    assert missing == []


def test_every_swift_source_is_referenced(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    assert set(SWIFT_SOURCES) <= set(resolved_paths(project))


def test_every_target_membership_names_a_phase_the_target_has(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    targets = {target.name: target for target in project.targets}
    for reference in project.file_references():
        for build_file in reference.build_files:
            phase = build_file.build_phase
            assert phase.target.raw_value in targets, f"{phase} names an unknown target"
            candidates = [entry for entry in targets[phase.target.raw_value].common_properties.build_phases if entry.kind is phase.kind]
            assert candidates, f"{phase} names a phase the target does not have"


def test_every_dependency_names_an_existing_target(written):
    project = XcodeProject.load(written / "Showcase.xcodeproj").project
    names = {target.name for target in project.targets}
    for target in project.targets:
        for dependency in target.common_properties.dependencies:
            if dependency.kind is TargetDependencyKind.LOCAL_TARGET:
                assert dependency.content.raw_value in names


def test_the_generated_project_is_already_canonical(written):
    once = (written / "Showcase.xcodeproj" / "project.xcproj").read_text(encoding="utf-8")
    assert XcodeProject.loads(once).dumps() == once


def test_the_generated_project_survives_the_command_line_tool(written, capsysbinary):
    assert main(["--update", str(written / "Showcase.xcodeproj")]) == 0
    reloaded = XcodeProject.load(written / "Showcase.xcodeproj")
    assert reloaded.project == Showcase.project().project


def test_the_swift_sources_are_written_with_content(written):
    for name in SWIFT_SOURCES:
        assert (written / name).read_text(encoding="utf-8").strip() != ""


def test_the_testable_source_declares_the_behaviour_the_test_asserts(written):
    calculator = (written / "Shared/Calculator.swift").read_text(encoding="utf-8")
    tests = (written / "AppTests/CalculatorTests.swift").read_text(encoding="utf-8")
    assert "func add(" in calculator
    assert "XCTAssertEqual(Calculator().add(2, 3), 5)" in tests


def test_the_bundle_holds_only_the_project_document(written):
    assert [path.name for path in (written / "Showcase.xcodeproj").iterdir()] == ["project.xcproj"]
