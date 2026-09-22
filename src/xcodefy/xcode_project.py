from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.project import Project
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.references.reference_kind import ReferenceKind
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.utilities.text import Text
from xcodefy.project_file import ProjectFile
from xcodefy.target_references import TargetReferences


@dataclass(slots=True)
class XcodeProject:
    project: Project
    path: Path | None = None

    @classmethod
    def loads(cls, text: str | bytes) -> Self:
        return cls(Project.from_json_text(text))

    @classmethod
    def load(cls, path: str | Path) -> Self:
        project_path = ProjectFile.resolve(path)
        return cls(Project.from_json_text(ProjectFile.read(project_path)), project_path)

    def dumps(self, options: EncodingOptions | None = None) -> str:
        return self.project.json_text(options)

    def save(self, path: str | Path | None = None) -> Path:
        project_path = ProjectFile.resolve(path) if path is not None else self.path
        if project_path is None:
            raise ValidationError("A path is required to save a project that was created in memory.")
        ProjectFile.write(project_path, self.dumps())
        self.path = project_path
        return project_path

    def validate(self) -> None:
        self.project.verify_reference_integrity()

    def target(self, name: str) -> Target:
        return self.project.target(name)

    def add_target(self, target: Target) -> Target:
        if any(existing.name == target.name for existing in self.project.targets):
            raise ValidationError(f"A target named {Text.smart_quoted(target.name)} already exists.")
        self.project.targets.append(target)
        return target

    def remove_target(self, name: str) -> Target:
        target = self.target(name)
        self.project.targets.remove(target)
        TargetReferences.remove(self.project, LocalTargetReference(name))
        return target

    def add_package(self, package: SwiftPackage) -> SwiftPackage:
        self.project.packages.append(package)
        return package

    def build_settings(self, target: str | None = None) -> dict[str, BuildSetting]:
        return self.project.build_settings if target is None else self.target(target).build_settings

    def set_build_setting(self, key: str, value: str | Sequence[str], target: str | None = None) -> None:
        setting = BuildSetting.of_string(value) if isinstance(value, str) else BuildSetting.of_array(value)
        self.build_settings(target)[key] = setting

    def remove_build_setting(self, key: str, target: str | None = None) -> None:
        self.build_settings(target).pop(key, None)

    def add_file(self, path: str, target: str | None = None, build_phase: BuildPhaseKind = BuildPhaseKind.SOURCES, build_phase_name: str | None = None, group: str | None = None) -> FileReference:
        reference = FileReference(FilePath.from_string_representation(path))
        if target is not None:
            reference.build_files.append(self._build_file(target, build_phase, build_phase_name))
        self._group_children(group).append(Reference.of_file(reference))
        return reference

    def _build_file(self, target: str, build_phase: BuildPhaseKind, build_phase_name: str | None) -> ProjectBuildFile:
        matched = self._matching_build_phase(target, build_phase, build_phase_name)
        phase = ProjectBuildPhaseReference.named(LocalTargetReference(target), build_phase, matched.name)
        return ProjectBuildFile(phase)

    def _matching_build_phase(self, target: str, build_phase: BuildPhaseKind, build_phase_name: str | None) -> BuildPhase:
        candidates = [phase for phase in self.target(target).common_properties.build_phases if phase.kind is build_phase]
        if build_phase_name is not None:
            candidates = [phase for phase in candidates if phase.name == build_phase_name]
        if not candidates:
            raise ValidationError(f"Target {Text.smart_quoted(target)} has no {Text.smart_quoted(build_phase.value)} build phase to add the file to.")
        if len(candidates) > 1:
            raise ValidationError(f"Target {Text.smart_quoted(target)} has several {Text.smart_quoted(build_phase.value)} build phases, so build_phase_name is required.")
        return candidates[0]

    def remove_file(self, path: str, group: str | None = None) -> FileReference:
        children = self._group_children(group)
        for index, reference in enumerate(children):
            if reference.kind is ReferenceKind.FILE_REFERENCE and reference.content.path.string_representation == path:
                children.pop(index)
                return reference.content
        raise KeyError(path)

    def files(self) -> Iterator[FileReference]:
        return self.project.file_references()

    def groups(self) -> Iterator[Group]:
        for reference in self.project.references():
            if reference.kind is ReferenceKind.GROUP:
                yield reference.content

    def group(self, name: str) -> Group:
        matches = [group for group in self.groups() if group.name == name]
        if not matches:
            raise KeyError(name)
        if len(matches) > 1:
            raise ValidationError(f"Group name {Text.smart_quoted(name)} is ambiguous.")
        return matches[0]

    def add_group(self, path: str, parent: str | None = None) -> Group:
        group = Group.named_after_path(FilePath.from_string_representation(path))
        self._group_children(parent).append(Reference.of_group(group))
        return group

    def _group_children(self, name: str | None) -> list[Reference]:
        return self.project.top_level_references if name is None else self.group(name).children
