from tests.support.instances import Instances
from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase_scope import BuildPhaseScope
from xcodefy.library.schema.build_phases.copy_files_build_phase_properties import CopyFilesBuildPhaseProperties
from xcodefy.library.schema.build_phases.script_build_phase_properties import ScriptBuildPhaseProperties
from xcodefy.library.schema.build_rules.build_rule import BuildRule
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.project import Project
from xcodefy.library.schema.references.common_reference_properties import CommonReferenceProperties
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.folder.exception_sets.build_phase_exception_set import BuildPhaseExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.common_exception_set_properties import CommonExceptionSetProperties
from xcodefy.library.schema.references.folder.exception_sets.exception_set_sense import ExceptionSetSense
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.target_exception_set import TargetExceptionSet
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.schema.references.line_ending import LineEnding
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.external_build_system_target_properties import ExternalBuildSystemTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.bundle_base_path import BundleBasePath
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.group_tree_anchored_reference import GroupTreeAnchoredReference
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.language import Language
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.marketing_version import MarketingVersion
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.product_type_id import ProductTypeID
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo
from xcodefy.library.schema.values.string_encoding import StringEncoding
from xcodefy.library.schema.values.text_encoding import TextEncoding


class Comprehensive:
    @staticmethod
    def folder_reference() -> Reference:
        member = FolderMemberID("Legacy.swift")
        common = CommonExceptionSetProperties(ExceptionSetSense.EXCLUSIONS, frozenset({member}))
        target_set = TargetExceptionSet(LocalTargetReference("App"), frozenset({FolderMemberID("Public.h")}), frozenset(), {}, common)
        phase_reference = ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.COPY, "Install")
        phase_set = BuildPhaseExceptionSet(phase_reference, CommonExceptionSetProperties())
        exceptions = [FolderExceptionSet.of_target(target_set), FolderExceptionSet.of_build_phase(phase_set)]
        folder = Folder(FilePath(FilePathBase.group(), "Sources"), None, frozenset({LocalTargetReference("App")}), exceptions)
        return Reference.of_folder(folder)

    @staticmethod
    def variant_group_reference() -> Reference:
        child = FileReference(FilePath(FilePathBase.group(), "en.lproj/Main.strings"))
        group = VariantGroup(FilePath(FilePathBase.group(), "Main.strings"), "Main.strings", None, CommonReferenceProperties(), [], [child])
        return Reference.of_variant_group(group)

    @staticmethod
    def version_group_reference() -> Reference:
        child = FileReference(FilePath(FilePathBase.group(), "Model.xcdatamodeld/Model.xcdatamodel"))
        current = GroupTreeReference.of_child_names(["Model.xcdatamodel"])
        group = VersionGroup(FilePath(FilePathBase.group(), "Model.xcdatamodeld"), "Model.xcdatamodeld", None, current, FileTypeID("wrapper.xcdatamodel"), CommonReferenceProperties(), [], [child])
        return Reference.of_version_group(group)

    @staticmethod
    def group_reference() -> Reference:
        build_file = ProjectBuildFile(ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.SOURCES))
        child = FileReference(FilePath(FilePathBase.group(), "App.swift"), None, None, None, TextEncoding.of(StringEncoding.UTF8), LineEnding.LINE_FEED, CommonReferenceProperties(True), [build_file])
        group = Group(FilePath(FilePathBase.group(), "App"), "App", None, CommonReferenceProperties(), [Reference.of_file(child)])
        return Reference.of_group(group)

    @staticmethod
    def application_target() -> Target:
        copy_phase = BuildPhase(BuildPhaseKind.COPY, CopyFilesBuildPhaseProperties(BuildPhaseProperties(None, "Install"), BundleBasePath.RESOURCES_DIR, "Assets", BuildPhaseScope.INSTALL))
        script_phase = BuildPhase(BuildPhaseKind.SCRIPT, ScriptBuildPhaseProperties(BuildPhaseProperties(None, "Lint"), "/bin/sh", "swiftlint\nexit 0", False, ["$(SRCROOT)/.swiftlint.yml"]))
        phases = [BuildPhase.of_kind(BuildPhaseKind.SOURCES), BuildPhase.of_kind(BuildPhaseKind.FRAMEWORKS), copy_phase, script_phase]
        dependencies = [TargetDependency.of_local_target(LocalTargetReference("Helper"))]
        rules = [BuildRule("com.apple.compilers.proxy.script", "Recompress", FileTypeID("image.png"), None, "echo recompress", [], [], ["$(DERIVED_FILE_DIR)/$(INPUT_FILE_BASE).png"])]
        settings = {"PRODUCT_NAME": BuildSetting.of_string("App"), "OTHER_SWIFT_FLAGS": BuildSetting.of_array(["-warnings-as-errors"])}
        configurations = [Configuration(ConfigurationName("Debug"), GroupTreeAnchoredReference(GroupTreeReference.of_child_names(["Config"]), NamePath.of_child_names(["Debug.xcconfig"])))]
        properties = CommonTargetProperties("App", ObjectID("APP"), None, dependencies, phases, rules, configurations, settings, None, ProductTypeID.from_abbreviated("application"), None, None, None, None, None, [Instances.populated_package_product_target_member()])
        return Target.native(properties)

    @staticmethod
    def external_target() -> Target:
        properties = CommonTargetProperties("Docs", ObjectID("DOCS"))
        return Target.external_build_system(ExternalBuildSystemTargetProperties(properties, "/usr/bin/make", "docs", "$(SRCROOT)", False))

    @staticmethod
    def project() -> Project:
        references = [Comprehensive.group_reference(), Comprehensive.folder_reference(), Comprehensive.variant_group_reference(), Comprehensive.version_group_reference()]
        packages = [Instances.populated_swift_package(), Instances.empty_swift_package()]
        configurations = [Configuration(ConfigurationName("Debug")), Configuration(ConfigurationName("Release"))]
        targets = [Comprehensive.application_target(), Target.aggregate(CommonTargetProperties("Helper", ObjectID("HELP"))), Comprehensive.external_target()]
        localization = ProjectLocalizationInfo(Language("en"), frozenset({Language("fr"), Language("pt-BR")}))
        settings = {"SDKROOT": BuildSetting.of_string("iphoneos")}
        imported = [Instances.populated_remote_product()]
        return Project(references, ConfigurationName("Debug"), localization, packages, configurations, settings, targets, frozenset(), True, MarketingVersion(27, 0), None, None, "example.com", "EX", None, ObjectID("PROJECT"), None, None, imported)
