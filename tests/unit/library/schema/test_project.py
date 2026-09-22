import pytest

from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.errors.decode_error import DecodeError
from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.project import DEFAULT_PRODUCTS_REFERENCE, Project
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.capability import Capability
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.object_id import ObjectID

MINIMAL = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }'


def test_a_minimal_project_decodes_and_re_encodes():
    project = Project.from_json_text(MINIMAL)
    assert project.default_configuration_name.raw_value == "Debug"
    assert Project.from_json_text(project.json_text()) == project


def test_json_data_matches_json_text():
    project = Project.from_json_text(MINIMAL)
    assert project.json_data() == project.json_text().encode("utf-8")


def test_the_products_group_defaults_to_the_products_name_path():
    assert Project.from_json_text(MINIMAL).products_group == DEFAULT_PRODUCTS_REFERENCE
    assert "products-group" not in Project.from_json_text(MINIMAL).json_text()


def test_an_explicit_null_products_group_is_preserved():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [], "products-group": null }'
    project = Project.from_json_text(text)
    assert project.products_group is None
    assert '"products-group": null' in project.json_text()


def test_a_custom_products_group_is_preserved():
    project = Project.from_json_text(MINIMAL)
    project.products_group = GroupTreeReference.of_child_names(["Built"])
    assert '"products-group": "Built"' in project.json_text()


def test_duplicate_target_names_are_rejected_on_encode_and_decode():
    project = Project.from_json_text(MINIMAL)
    project.targets = [Target.native(CommonTargetProperties("App", ObjectID("T1"))), Target.native(CommonTargetProperties("App", ObjectID("T2")))]
    with pytest.raises(ValidationError, match="“App” is used multiple times"):
        project.json_text()


def test_several_duplicate_target_names_are_listed():
    project = Project.from_json_text(MINIMAL)
    names = ["A", "A", "B", "B"]
    project.targets = [Target.native(CommonTargetProperties(name, ObjectID(name + str(index)))) for index, name in enumerate(names)]
    with pytest.raises(ValidationError, match="“A” and “B” are used multiple times"):
        project.verify_reference_integrity()


def test_an_unsatisfied_capability_is_rejected_with_the_tool_name():
    text = '{ "required-capabilities": ["glow in the dark"], "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }'
    with pytest.raises(DecodeError, match="requires a newer version of Xcode with support for glow in the dark"):
        Project.from_json_text(text)


def test_several_unsatisfied_capabilities_are_listed():
    text = '{ "required-capabilities": ["a", "b"], "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [] }'
    with pytest.raises(DecodeError, match="support for a and b"):
        Project.from_json_text(text)


def test_a_known_capability_is_accepted():
    project = Project.from_json_text(MINIMAL)
    project.required_capabilities = frozenset({Capability.known_capability_for_testing()})
    assert Project.from_json_text(project.json_text()).required_capabilities == project.required_capabilities


def test_a_target_is_found_by_name_and_ambiguity_is_reported():
    project = Project.from_json_text(MINIMAL)
    project.targets = [Target.native(CommonTargetProperties("App", ObjectID("T1")))]
    assert project.target("App").name == "App"
    with pytest.raises(KeyError):
        project.target("Missing")
    project.targets.append(Target.native(CommonTargetProperties("App", ObjectID("T2"))))
    with pytest.raises(ValidationError, match="is ambiguous"):
        project.target("App")


def test_walking_the_tree_visits_nested_group_children():
    inner = Reference.of_file(FileReference())
    group = Reference.of_group(Group(children=[inner]))
    project = Project.from_json_text(MINIMAL)
    project.top_level_references = [group]
    assert list(project.references()) == [group, inner]


def test_a_folder_reference_is_not_walked_into():
    folder = Reference.of_folder(Instances.populated_folder())
    project = Project.from_json_text(MINIMAL)
    project.top_level_references = [folder]
    assert list(project.references()) == [folder]


def test_a_fully_populated_project_round_trips():
    RoundTrip.expect_equal(Instances.populated_project(), Project)


def test_an_empty_project_round_trips():
    RoundTrip.expect_equal(Instances.empty_project(), Project)


def test_the_field_order_follows_the_reference_layout():
    keys = [line.strip().split('"')[1] for line in Instances.populated_project().json_text().splitlines() if line.startswith('  "')]
    expected = [
        "required-capabilities",
        "id",
        "root-group-debug-id",
        "configuration-list-debug-id",
        "organization",
        "class-prefix",
        "default-configuration",
        "configurations",
        "localizations",
        "imported-products",
        "packages",
        "files",
        "targets",
        "build-settings",
        "products-group",
        "last-upgrade",
        "last-swift-update",
        "last-swift-migration",
    ]
    assert keys == expected


def test_re_encoding_a_canonical_document_changes_nothing():
    once = Instances.populated_project().json_text()
    assert Project.from_json_text(once).json_text() == once


def test_a_document_with_comments_and_json5_syntax_normalises():
    text = "{\n  // leading\n  'default-configuration': 'Debug',\n  localizations: { development: 'en', },\n  files: [],\n}"
    assert Project.from_json_text(text).json_text() == Project.from_json_text(MINIMAL).json_text()


def test_reading_an_invalid_document_always_raises_a_decode_error():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [], "targets": [ { "name": "A", "id": "1" }, { "name": "A", "id": "2" } ] }'
    with pytest.raises(DecodeError, match="must be unique"):
        Project.from_json_text(text)


def test_writing_an_invalid_project_raises_a_validation_error():
    project = Project.from_json_text(MINIMAL)
    project.targets = [Target.native(CommonTargetProperties("A", ObjectID("1"))), Target.native(CommonTargetProperties("A", ObjectID("2")))]
    with pytest.raises(ValidationError, match="must be unique"):
        project.json_text()


def test_the_fields_the_format_requires_have_no_default():
    with pytest.raises(TypeError):
        Project()


@pytest.mark.parametrize("key", ["organization", "class-prefix", "last-upgrade"])
def test_a_present_only_project_field_rejects_an_explicit_null(key):
    text = f'{{ "default-configuration": "Debug", "localizations": {{ "development": "en" }}, "files": [], "{key}": null }}'
    with pytest.raises(DecodeError):
        Project.from_json_text(text)


def test_an_annotated_decode_error_keeps_the_original_as_its_cause():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "path": 1 } ] }'
    with pytest.raises(DecodeError) as caught:
        Project.from_json_text(text)
    error = caught.value
    assert error.coding_path == "/files[0]/path"
    assert isinstance(error.__cause__, DecodeError)
    assert error.__cause__ is not error
    assert error.__cause__.coding_path is None


def test_a_non_basic_plane_character_written_as_a_surrogate_pair_survives(tmp_path):
    escape = r"\ud83d\ude05"
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "path": "' + escape + '.swift" } ] }'
    project = Project.from_json_text(text)
    assert project.top_level_references[0].content.path.string_representation == chr(0x1F605) + ".swift"
    target = tmp_path / "project.xcproj"
    target.write_text(project.json_text(), encoding="utf-8")
    assert Project.from_json_text(target.read_text(encoding="utf-8")) == project


def nested_group_document(levels):
    inner = '{ "path": "leaf.swift" }'
    for _ in range(levels):
        inner = '{ "kind": "group", "path": "g", "children": [ ' + inner + " ] }"
    return '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ ' + inner + " ] }"


def test_the_deepest_accepted_document_still_decodes_and_re_encodes():
    project = Project.from_json_text(nested_group_document(62))
    assert project.json_text() == Project.from_json_text(project.json_text()).json_text()


def test_a_document_nested_past_the_limit_is_rejected_cleanly():
    with pytest.raises(DecodeError, match="Nesting is deeper"):
        Project.from_json_text(nested_group_document(63))


def test_every_file_in_the_project_is_walked_including_grouped_children():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "path": "top.swift" }, { "kind": "group", "path": "G", "children": [ { "path": "nested.swift" } ] }, { "kind": "variant-group", "path": "Main.strings", "children": [ { "path": "en.strings" } ] }, { "kind": "version-group", "path": "M.xcdatamodeld", "children": [ { "path": "M.xcdatamodel" } ] } ] }'
    project = Project.from_json_text(text)
    walked = [reference.path.string_representation for reference in project.file_references()]
    assert sorted(walked) == ["M.xcdatamodel", "en.strings", "nested.swift", "top.swift"]
    assert len(walked) == len(set(walked))


def test_a_folder_contributes_no_file_references():
    text = '{ "default-configuration": "Debug", "localizations": { "development": "en" }, "files": [ { "kind": "folder", "path": "Src" } ] }'
    assert list(Project.from_json_text(text).file_references()) == []
