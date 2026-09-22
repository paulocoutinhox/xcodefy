import pytest

from tests.support.instances import Instances
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.copy_files_build_phase_properties import CopyFilesBuildPhaseProperties
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.xcode_project import XcodeProject

MINIMAL = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }\n'


def project() -> XcodeProject:
    return XcodeProject.loads(MINIMAL)


def with_app() -> XcodeProject:
    loaded = project()
    phases = [BuildPhase.of_kind(BuildPhaseKind.SOURCES), BuildPhase(BuildPhaseKind.COPY, CopyFilesBuildPhaseProperties(BuildPhaseProperties(None, "Install")))]
    loaded.add_target(Target.native(CommonTargetProperties("App", ObjectID("T1"), build_phases=phases)))
    return loaded


def test_loading_and_dumping_is_idempotent():
    loaded = project()
    once = loaded.dumps()
    assert XcodeProject.loads(once).dumps() == once


def test_adding_a_duplicate_target_is_rejected():
    loaded = with_app()
    with pytest.raises(ValidationError, match="already exists"):
        loaded.add_target(Target.native(CommonTargetProperties("App", ObjectID("T2"))))


def test_targets_can_be_added_and_removed():
    loaded = with_app()
    assert loaded.target("App").name == "App"
    assert loaded.remove_target("App").name == "App"
    with pytest.raises(KeyError):
        loaded.target("App")


def test_an_ambiguous_target_name_is_reported():
    loaded = with_app()
    loaded.project.targets.append(Target.native(CommonTargetProperties("App", ObjectID("T2"))))
    with pytest.raises(ValidationError, match="ambiguous"):
        loaded.target("App")


def test_duplicate_target_names_fail_verification():
    loaded = with_app()
    loaded.project.targets.append(Target.native(CommonTargetProperties("App", ObjectID("T2"))))
    with pytest.raises(ValidationError, match="must be unique"):
        loaded.validate()


def test_files_can_be_added_to_the_top_level_and_to_a_group():
    loaded = with_app()
    loaded.add_group("Sources")
    loaded.add_file("main.swift", target="App", group="Sources")
    loaded.add_file("README.md")
    assert sorted(reference.path.string_representation for reference in loaded.files()) == ["README.md", "main.swift"]


def test_a_file_can_carry_a_named_build_phase():
    loaded = with_app()
    reference = loaded.add_file("main.swift", target="App", build_phase=BuildPhaseKind.COPY, build_phase_name="Install")
    assert str(reference.build_files[0].build_phase) == "App/copy/Install"


def test_a_resolved_reference_carries_the_phase_name_even_when_it_was_not_asked_for():
    loaded = with_app()
    reference = loaded.add_file("main.swift", target="App", build_phase=BuildPhaseKind.COPY)
    assert str(reference.build_files[0].build_phase) == "App/copy/Install"


def test_a_path_is_stored_relative_to_the_group_it_is_added_to():
    loaded = with_app()
    loaded.add_group("Sources")
    added = loaded.add_file("Feature.swift", group="Sources")
    assert added.path.string_representation == "Feature.swift"
    assert loaded.group("Sources").path.string_representation == "Sources"


def test_a_group_is_stored_relative_to_its_parent():
    loaded = with_app()
    loaded.add_group("Sources")
    nested = loaded.add_group("Helpers", parent="Sources")
    assert nested.path.string_representation == "Helpers"
    assert nested.name == "Helpers"


def test_adding_a_file_to_a_target_without_the_phase_is_refused():
    loaded = project()
    loaded.add_target(Target.native(CommonTargetProperties("Bare", ObjectID("T9"))))
    with pytest.raises(ValidationError, match="has no .* build phase"):
        loaded.add_file("main.swift", target="Bare")


def test_adding_a_file_to_an_ambiguous_phase_is_refused():
    loaded = project()
    phases = [BuildPhase(BuildPhaseKind.COPY, CopyFilesBuildPhaseProperties(BuildPhaseProperties(None, name))) for name in ("One", "Two")]
    loaded.add_target(Target.native(CommonTargetProperties("Twice", ObjectID("T8"), build_phases=phases)))
    with pytest.raises(ValidationError, match="build_phase_name is required"):
        loaded.add_file("main.swift", target="Twice", build_phase=BuildPhaseKind.COPY)
    resolved = loaded.add_file("main.swift", target="Twice", build_phase=BuildPhaseKind.COPY, build_phase_name="Two")
    assert str(resolved.build_files[0].build_phase) == "Twice/copy/Two"


def test_removing_a_missing_file_raises():
    loaded = project()
    with pytest.raises(KeyError):
        loaded.remove_file("missing.swift")


def test_files_can_be_removed():
    loaded = project()
    loaded.add_file("main.swift")
    assert loaded.remove_file("main.swift").path.string_representation == "main.swift"
    assert list(loaded.files()) == []


def test_groups_can_be_looked_up_and_are_checked_for_ambiguity():
    loaded = project()
    loaded.add_group("Sources")
    assert loaded.group("Sources").name == "Sources"
    loaded.add_group("Sources")
    with pytest.raises(ValidationError, match="ambiguous"):
        loaded.group("Sources")


def test_a_missing_group_raises():
    loaded = project()
    with pytest.raises(KeyError):
        loaded.group("Sources")


def test_build_settings_can_be_set_and_removed_on_the_project_and_a_target():
    loaded = with_app()
    loaded.set_build_setting("SDKROOT", "iphoneos")
    loaded.set_build_setting("OTHER_FLAGS", ["-O"], target="App")
    assert loaded.build_settings()["SDKROOT"].string == "iphoneos"
    assert loaded.build_settings("App")["OTHER_FLAGS"].array == ("-O",)
    loaded.remove_build_setting("SDKROOT")
    loaded.remove_build_setting("MISSING")
    assert "SDKROOT" not in loaded.build_settings()


def test_packages_can_be_added():
    loaded = project()
    package = loaded.add_package(Instances.populated_swift_package())
    assert loaded.project.packages == [package]


def test_a_project_can_be_saved_and_reloaded(tmp_path):
    loaded = with_app()
    saved = loaded.save(tmp_path / "Demo.xcodeproj")
    assert saved == tmp_path / "Demo.xcodeproj" / "project.xcproj"
    assert XcodeProject.load(tmp_path / "Demo.xcodeproj").dumps() == loaded.dumps()
    assert loaded.save() == saved


def test_saving_a_project_without_a_path_is_rejected():
    with pytest.raises(ValidationError, match="path is required"):
        project().save()


def test_a_populated_project_round_trips_through_text():
    original = Instances.populated_project()
    assert XcodeProject.loads(original.json_text()).project == original
