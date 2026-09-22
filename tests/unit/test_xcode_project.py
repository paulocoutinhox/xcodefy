import pytest

from tests.support.instances import Instances
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.xcode_project import XcodeProject

MINIMAL = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }\n'


def loaded():
    project = XcodeProject.loads(MINIMAL)
    phases = [BuildPhase.of_kind(BuildPhaseKind.SOURCES)]
    project.add_target(Target.native(CommonTargetProperties("App", ObjectID("T1"), build_phases=phases)))
    return project


def test_a_project_is_loaded_from_text():
    assert XcodeProject.loads(MINIMAL).project.default_configuration_name.raw_value == "Debug"
    assert XcodeProject.loads(MINIMAL).path is None


def test_the_encoding_options_are_honoured():
    assert not XcodeProject.loads(MINIMAL).dumps(EncodingOptions(add_trailing_newline=False)).endswith("\n\n")


def test_adding_a_file_to_a_missing_target_is_rejected():
    with pytest.raises(KeyError):
        loaded().add_file("main.swift", target="Missing")


def test_adding_a_file_to_a_missing_group_is_rejected():
    with pytest.raises(KeyError):
        loaded().add_file("main.swift", group="Missing")


def test_a_group_can_be_nested_inside_another_group():
    project = loaded()
    project.add_group("Sources")
    project.add_group("Helpers", parent="Sources")
    assert sorted(group.name for group in project.groups()) == ["Helpers", "Sources"]


def test_removing_a_file_from_a_group_leaves_the_rest_untouched():
    project = loaded()
    project.add_group("Sources")
    project.add_file("a.swift", group="Sources")
    project.add_file("b.swift", group="Sources")
    project.remove_file("a.swift", group="Sources")
    assert [reference.path.string_representation for reference in project.files()] == ["b.swift"]


def test_removing_a_missing_file_from_a_group_is_reported():
    project = loaded()
    project.add_group("Sources")
    with pytest.raises(KeyError):
        project.remove_file("a.swift", group="Sources")


def test_removing_a_missing_target_is_reported():
    with pytest.raises(KeyError):
        loaded().remove_target("Missing")


def test_the_manipulation_api_keeps_the_document_valid():
    project = loaded()
    project.add_group("Sources")
    project.add_file("main.swift", target="App", group="Sources")
    project.set_build_setting("SDKROOT", "iphoneos")
    project.set_build_setting("OTHER_FLAGS", ["-O"], target="App")
    project.add_package(Instances.populated_swift_package())
    project.validate()
    assert XcodeProject.loads(project.dumps()).project == project.project


def test_saving_records_the_path_for_later_saves(tmp_path):
    project = loaded()
    project.save(tmp_path / "Demo.xcodeproj")
    project.set_build_setting("SDKROOT", "iphoneos")
    project.save()
    assert "SDKROOT" in XcodeProject.load(tmp_path / "Demo.xcodeproj").project.build_settings


def test_saving_to_a_bare_file_path_works(tmp_path):
    project = loaded()
    saved = project.save(tmp_path / "project.xcproj")
    assert saved == tmp_path / "project.xcproj"


def test_validation_surfaces_duplicate_target_names():
    project = loaded()
    project.project.targets.append(Target.native(CommonTargetProperties("App", ObjectID("T2"))))
    with pytest.raises(ValidationError, match="must be unique"):
        project.validate()


def test_removing_a_file_skips_groups_and_earlier_files():
    project = loaded()
    project.add_group("Sources")
    project.add_file("a.swift")
    project.add_file("b.swift")
    project.remove_file("b.swift")
    assert [reference.path.string_representation for reference in project.files()] == ["a.swift"]


def test_saving_replaces_the_project_without_leaving_a_staging_file(tmp_path):
    project = loaded()
    project.save(tmp_path / "Demo.xcodeproj")
    project.set_build_setting("SDKROOT", "iphoneos")
    project.save()
    assert sorted(path.name for path in (tmp_path / "Demo.xcodeproj").iterdir()) == ["project.xcproj"]


def test_removing_a_target_also_removes_what_referenced_it():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "path": "a.swift", "target-membership": [ "App/compile-sources" ] }, { "kind": "folder", "path": "Src", "target-membership": [ "App" ] } ], "targets": [ { "name": "App", "id": "A", "build-phases": [ "compile-sources" ] }, { "name": "Tests", "id": "T", "dependencies": [ "App" ], "test-host-target": "App" } ] }'
    project = XcodeProject.loads(text)
    project.remove_target("App")
    assert "App" not in project.dumps()
    assert XcodeProject.loads(project.dumps()).project == project.project


def test_files_yields_the_children_of_variant_and_version_groups():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "kind": "variant-group", "path": "Main.strings", "children": [ { "path": "en.strings" } ] } ] }'
    project = XcodeProject.loads(text)
    assert [reference.path.string_representation for reference in project.files()] == ["en.strings"]


def test_loading_a_file_that_is_not_utf8_reports_a_decode_error(tmp_path):
    bundle = tmp_path / "Demo.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_bytes(b'{ "path": "caf\xe9.swift" }')
    with pytest.raises(DecodeError, match="not valid UTF-8"):
        XcodeProject.load(bundle)


def test_a_project_with_a_byte_order_mark_loads_and_is_written_without_one(tmp_path):
    bundle = tmp_path / "Demo.xcodeproj"
    bundle.mkdir()
    (bundle / "project.xcproj").write_bytes(b"\xef\xbb\xbf" + MINIMAL.encode("utf-8"))
    project = XcodeProject.load(bundle)
    project.save()
    assert not (bundle / "project.xcproj").read_bytes().startswith(b"\xef\xbb\xbf")
