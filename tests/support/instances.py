from xcodefy.library.schema.build_files.build_file_attributes import BuildFileAttributes
from xcodefy.library.schema.build_files.build_file_properties import BuildFileProperties
from xcodefy.library.schema.build_files.code_generation import CodeGeneration
from xcodefy.library.schema.build_files.code_generation_visibility import CodeGenerationVisibility
from xcodefy.library.schema.build_files.header_preservation import HeaderPreservation
from xcodefy.library.schema.build_files.header_role import HeaderRole
from xcodefy.library.schema.build_files.mach_interface_generation import MachInterfaceGeneration
from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.build_files.target_build_file import TargetBuildFile
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.apple_script_build_phase_properties import AppleScriptBuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase import BuildPhase
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.build_phases.build_phase_properties import BuildPhaseProperties
from xcodefy.library.schema.build_phases.build_phase_scope import BuildPhaseScope
from xcodefy.library.schema.build_phases.copy_files_build_phase_properties import CopyFilesBuildPhaseProperties
from xcodefy.library.schema.build_phases.script_build_phase_properties import ScriptBuildPhaseProperties
from xcodefy.library.schema.build_rules.build_rule import BuildRule
from xcodefy.library.schema.configuration import Configuration
from xcodefy.library.schema.packages.local_swift_package import LocalSwiftPackage
from xcodefy.library.schema.packages.remote_swift_package import RemoteSwiftPackage
from xcodefy.library.schema.packages.swift_package import SwiftPackage
from xcodefy.library.schema.packages.swift_package_location import SwiftPackageLocation
from xcodefy.library.schema.packages.swift_package_version_constraint import SwiftPackageVersionConstraint
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
from xcodefy.library.schema.target.dependencies.remote_product import RemoteProduct
from xcodefy.library.schema.target.dependencies.remote_target import RemoteTarget
from xcodefy.library.schema.target.dependencies.swift_package_product_reference import SwiftPackageProductReference
from xcodefy.library.schema.target.dependencies.swift_package_product_target_member import SwiftPackageProductTargetMember
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.external_build_system_target_properties import ExternalBuildSystemTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.asset_tag import AssetTag
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.bundle_base_path import BundleBasePath
from xcodefy.library.schema.values.capability import Capability
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_path_base import FilePathBase
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.group_tree_anchored_reference import GroupTreeAnchoredReference
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.language import Language
from xcodefy.library.schema.values.legacy_provisioning_style import LegacyProvisioningStyle
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.marketing_version import MarketingVersion
from xcodefy.library.schema.values.multiline_text import MultilineText
from xcodefy.library.schema.values.name_path import NamePath
from xcodefy.library.schema.values.name_path_component import NamePathComponent
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.platform_filter import PlatformFilter
from xcodefy.library.schema.values.product_type_id import ProductTypeID
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo
from xcodefy.library.schema.values.relative_reference import RelativeReference
from xcodefy.library.schema.values.string_encoding import StringEncoding
from xcodefy.library.schema.values.swift_package_name import SwiftPackageName
from xcodefy.library.schema.values.swift_package_product_type import SwiftPackageProductType
from xcodefy.library.schema.values.text_encoding import TextEncoding


class Instances:
    @staticmethod
    def object_id() -> ObjectID:
        return ObjectID("0123456789ABCDEF")

    @staticmethod
    def other_object_id() -> ObjectID:
        return ObjectID("FEDCBA9876543210")

    @staticmethod
    def populated_file_path() -> FilePath:
        return FilePath(FilePathBase.absolute(), "/Sources/Foo.swift")

    @staticmethod
    def empty_file_path() -> FilePath:
        return FilePath()

    @staticmethod
    def populated_name_path() -> NamePath:
        return NamePath((NamePathComponent.of_relative(RelativeReference.PARENT), NamePathComponent.child("Sources"), NamePathComponent.child("Foo.swift")))

    @staticmethod
    def populated_group_tree_reference() -> GroupTreeReference:
        return GroupTreeReference.of_name_path(Instances.populated_name_path())

    @staticmethod
    def populated_anchored_reference() -> GroupTreeAnchoredReference:
        return GroupTreeAnchoredReference(Instances.populated_group_tree_reference(), Instances.populated_name_path())

    @staticmethod
    def populated_build_file_attributes() -> BuildFileAttributes:
        return BuildFileAttributes(HeaderRole.PUBLIC, MachInterfaceGeneration.BOTH, True, True, CodeGeneration.SKIP, HeaderPreservation.REMOVE_ON_COPY, True, CodeGenerationVisibility.PUBLIC)

    @staticmethod
    def populated_build_file_properties() -> BuildFileProperties:
        return BuildFileProperties(frozenset({PlatformFilter("ios")}), Instances.populated_build_file_attributes(), "--go-fast", frozenset({AssetTag("release-asset")}))

    @staticmethod
    def populated_project_build_phase_reference() -> ProjectBuildPhaseReference:
        return ProjectBuildPhaseReference.named(LocalTargetReference("App"), BuildPhaseKind.SCRIPT, "Install man pages")

    @staticmethod
    def empty_project_build_phase_reference() -> ProjectBuildPhaseReference:
        return ProjectBuildPhaseReference.named(LocalTargetReference(""), BuildPhaseKind.SOURCES)

    @staticmethod
    def populated_target_build_phase_reference() -> TargetBuildPhaseReference:
        return TargetBuildPhaseReference.named(BuildPhaseKind.COPY, "Install man pages")

    @staticmethod
    def empty_target_build_phase_reference() -> TargetBuildPhaseReference:
        return TargetBuildPhaseReference.named(BuildPhaseKind.HEADERS)

    @staticmethod
    def populated_project_build_file() -> ProjectBuildFile:
        return ProjectBuildFile(Instances.populated_project_build_phase_reference(), Instances.populated_build_file_properties(), Instances.object_id())

    @staticmethod
    def empty_project_build_file() -> ProjectBuildFile:
        return ProjectBuildFile(Instances.empty_project_build_phase_reference())

    @staticmethod
    def populated_target_build_file() -> TargetBuildFile:
        return TargetBuildFile(Instances.populated_target_build_phase_reference(), Instances.populated_build_file_properties(), Instances.object_id())

    @staticmethod
    def empty_target_build_file() -> TargetBuildFile:
        return TargetBuildFile(Instances.empty_target_build_phase_reference())

    @staticmethod
    def populated_script_properties() -> ScriptBuildPhaseProperties:
        base = BuildPhaseProperties(Instances.object_id(), "Run Script")
        return ScriptBuildPhaseProperties(base, "/bin/sh", "echo hello", True, ["$(SRCROOT)/in.txt"], ["$(SRCROOT)/in.xcfilelist"], ["$(DERIVED_FILE_DIR)/out.txt"], ["$(DERIVED_FILE_DIR)/out.xcfilelist"], "$(DERIVED_FILE_DIR)/deps.d", True, BuildPhaseScope.INSTALL)

    @staticmethod
    def populated_copy_properties() -> CopyFilesBuildPhaseProperties:
        base = BuildPhaseProperties(Instances.object_id(), "Copy Files")
        return CopyFilesBuildPhaseProperties(base, BundleBasePath.RESOURCES_DIR, "Subfolder", BuildPhaseScope.INSTALL)

    @staticmethod
    def populated_apple_script_properties() -> AppleScriptBuildPhaseProperties:
        base = BuildPhaseProperties(Instances.object_id(), "Run AppleScript")
        return AppleScriptBuildPhaseProperties(base, True, "MyContext")

    @staticmethod
    def populated_build_rule() -> BuildRule:
        return BuildRule("sh", "Custom Rule", FileTypeID("sourcecode.swift"), "*.swift", "swiftc $INPUT_FILE_PATH", ["$(SRCROOT)/in.swift"], ["$(SRCROOT)/in.xcfilelist"], ["$(DERIVED_FILE_DIR)/out.o"], ["$(DERIVED_FILE_DIR)/out.xcfilelist"], ["-O"], "$(DERIVED_FILE_DIR)/deps.d", True, Instances.object_id())

    @staticmethod
    def populated_common_exception_set_properties() -> CommonExceptionSetProperties:
        member = FolderMemberID("File1.swift")
        return CommonExceptionSetProperties(ExceptionSetSense.EXCLUSIONS, frozenset({member}), {member: frozenset({PlatformFilter("ios")})}, {member: Instances.populated_build_file_attributes()}, {member: frozenset({AssetTag("release-asset")})})

    @staticmethod
    def populated_target_exception_set() -> TargetExceptionSet:
        return TargetExceptionSet(LocalTargetReference("App"), frozenset({FolderMemberID("Foo.h")}), frozenset({FolderMemberID("Bar.h")}), {FolderMemberID("Foo.h"): "-O"}, Instances.populated_common_exception_set_properties())

    @staticmethod
    def populated_build_phase_exception_set() -> BuildPhaseExceptionSet:
        return BuildPhaseExceptionSet(Instances.populated_project_build_phase_reference(), Instances.populated_common_exception_set_properties())

    @staticmethod
    def populated_file_reference() -> FileReference:
        return FileReference(Instances.populated_file_path(), Instances.object_id(), FileTypeID("sourcecode.swift"), "abc123", TextEncoding.of(StringEncoding.UTF8), LineEnding.LINE_FEED, CommonReferenceProperties(True), [Instances.populated_project_build_file()])

    @staticmethod
    def populated_folder() -> Folder:
        exceptions = [FolderExceptionSet.of_target(Instances.populated_target_exception_set())]
        return Folder(Instances.populated_file_path(), Instances.object_id(), frozenset({LocalTargetReference("App")}), exceptions, {FolderMemberID("File1.swift"): FileTypeID("sourcecode.swift")}, frozenset({FolderMemberID("OpaqueFolder")}), CommonReferenceProperties(True))

    @staticmethod
    def populated_group() -> Group:
        return Group(Instances.populated_file_path(), "Sources", Instances.object_id(), CommonReferenceProperties(True), [Reference.of_file(Instances.populated_file_reference())])

    @staticmethod
    def populated_variant_group() -> VariantGroup:
        return VariantGroup(Instances.populated_file_path(), "Variants", Instances.object_id(), CommonReferenceProperties(True), [Instances.populated_project_build_file()], [Instances.populated_file_reference()])

    @staticmethod
    def populated_version_group() -> VersionGroup:
        return VersionGroup(Instances.populated_file_path(), "Model", Instances.object_id(), Instances.populated_group_tree_reference(), FileTypeID("sourcecode.swift"), CommonReferenceProperties(True), [Instances.populated_project_build_file()], [Instances.populated_file_reference()])

    @staticmethod
    def populated_remote_target() -> RemoteTarget:
        return RemoteTarget(Instances.populated_group_tree_reference(), "OtherTarget", Instances.object_id())

    @staticmethod
    def populated_remote_product() -> RemoteProduct:
        return RemoteProduct(Instances.populated_group_tree_reference(), "MyFramework", Instances.object_id(), "MyFramework.framework", FileTypeID("sourcecode.swift"), [Instances.populated_project_build_file()])

    @staticmethod
    def populated_package_product_reference() -> SwiftPackageProductReference:
        return SwiftPackageProductReference("helper", SwiftPackageProductType.BUILD_TOOL_PLUGIN, SwiftPackageName("SuperUseful"), Instances.object_id())

    @staticmethod
    def populated_package_product_target_member() -> SwiftPackageProductTargetMember:
        return SwiftPackageProductTargetMember(Instances.populated_package_product_reference(), Instances.populated_target_build_file())

    @staticmethod
    def populated_swift_package() -> SwiftPackage:
        constraint = SwiftPackageVersionConstraint.up_to_next_major_version("1.4")
        remote = RemoteSwiftPackage("https://github.com/example/Package.git", constraint)
        return SwiftPackage(SwiftPackageLocation.of_remote(remote))

    @staticmethod
    def empty_swift_package() -> SwiftPackage:
        return SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage()))

    @staticmethod
    def populated_common_target_properties() -> CommonTargetProperties:
        dependencies = [TargetDependency.of_remote_target(Instances.populated_remote_target(), frozenset({PlatformFilter("ios")}))]
        phases = [BuildPhase(BuildPhaseKind.SCRIPT, Instances.populated_script_properties())]
        configurations = [Configuration(ConfigurationName("Debug"), Instances.populated_anchored_reference(), Instances.object_id())]
        settings = {"SWIFT_VERSION": BuildSetting.of_string("Setting")}
        return CommonTargetProperties(
            "App",
            Instances.object_id(),
            Instances.object_id(),
            dependencies,
            phases,
            [Instances.populated_build_rule()],
            configurations,
            settings,
            None,
            ProductTypeID("com.apple.product-type.application"),
            LocalTargetReference("App"),
            LegacyProvisioningStyle.AUTOMATIC,
            "MyTeamID",
            MarketingVersion(27, 1, 2),
            MarketingVersion(27, 1, 2),
            [Instances.populated_package_product_target_member()],
        )

    @staticmethod
    def empty_common_target_properties() -> CommonTargetProperties:
        dependencies = [TargetDependency.of_local_target(LocalTargetReference(""))]
        phases = [BuildPhase(BuildPhaseKind.SOURCES, BuildPhaseProperties())]
        return CommonTargetProperties("", Instances.other_object_id(), None, dependencies, phases, [BuildRule()])

    @staticmethod
    def populated_external_target_properties() -> ExternalBuildSystemTargetProperties:
        return ExternalBuildSystemTargetProperties(Instances.populated_common_target_properties(), "/usr/bin/external-tool", "--glow-in-the-dark true", "/shared/build", True)

    @staticmethod
    def populated_localization_info() -> ProjectLocalizationInfo:
        return ProjectLocalizationInfo(Language("en"), frozenset({Language("Base")}))

    @staticmethod
    def populated_project() -> Project:
        return Project(
            [Reference.of_file(Instances.populated_file_reference())],
            ConfigurationName("Debug"),
            Instances.populated_localization_info(),
            [Instances.populated_swift_package()],
            [Configuration(ConfigurationName("Debug"), Instances.populated_anchored_reference(), Instances.object_id()), Configuration(ConfigurationName("Release"))],
            {"SDKROOT": BuildSetting.of_string("Setting")},
            [Target.native(Instances.populated_common_target_properties())],
            frozenset({Capability.known_capability_for_testing()}),
            True,
            MarketingVersion(27, 1, 2),
            MarketingVersion(27, 1, 2),
            MarketingVersion(27, 1, 2),
            "example.com",
            "EX",
            Instances.populated_group_tree_reference(),
            Instances.object_id(),
            Instances.object_id(),
            Instances.object_id(),
            [Instances.populated_remote_product()],
        )

    @staticmethod
    def empty_project() -> Project:
        return Project([], ConfigurationName(""), ProjectLocalizationInfo(Language("en")), [], [], {}, [], frozenset(), False, None, None, None, None, None, None, None, None, None, [])


ROUND_TRIP_CASES = [
    (AssetTag("release-asset"), AssetTag),
    (AssetTag(""), AssetTag),
    (ConfigurationName("Debug"), ConfigurationName),
    (FileTypeID("sourcecode.swift"), FileTypeID),
    (FolderMemberID("Sources/Foo.swift"), FolderMemberID),
    (Language("en"), Language),
    (LocalTargetReference("App"), LocalTargetReference),
    (ObjectID("0123456789ABCDEF"), ObjectID),
    (PlatformFilter("ios"), PlatformFilter),
    (ProductTypeID("com.apple.product-type.application"), ProductTypeID),
    (SwiftPackageName("SuperUseful"), SwiftPackageName),
    (Capability.known_capability_for_testing(), Capability),
    (MarketingVersion(27, 1, 2), MarketingVersion),
    (MarketingVersion(27, 0, 0), MarketingVersion),
    (MultilineText('#!/usr/bin/sh\necho "Hello World"\n'), MultilineText),
    (MultilineText(""), MultilineText),
    (MultilineText("\n"), MultilineText),
    (MultilineText("\n\n"), MultilineText),
    (MultilineText("\n\n\n"), MultilineText),
    (BuildSetting.of_string("Setting"), BuildSetting),
    (BuildSetting.of_array([]), BuildSetting),
    (BuildSetting.of_array(["A", "B"]), BuildSetting),
    (TextEncoding.of(StringEncoding.UTF8), TextEncoding),
    (TextEncoding(23418341), TextEncoding),
    (Instances.populated_file_path(), FilePath),
    (Instances.empty_file_path(), FilePath),
    (Instances.populated_name_path(), NamePath),
    (NamePath(), NamePath),
    (NamePathComponent.of_relative(RelativeReference.PARENT), NamePathComponent),
    (NamePathComponent.child(""), NamePathComponent),
    (NamePathComponent.child("/"), NamePathComponent),
    (Instances.populated_group_tree_reference(), GroupTreeReference),
    (GroupTreeReference.of_object_id(Instances.object_id()), GroupTreeReference),
    (Instances.populated_anchored_reference(), GroupTreeAnchoredReference),
    (GroupTreeAnchoredReference(Instances.populated_group_tree_reference()), GroupTreeAnchoredReference),
    (Instances.populated_localization_info(), ProjectLocalizationInfo),
    (Instances.populated_build_file_attributes(), BuildFileAttributes),
    (BuildFileAttributes(), BuildFileAttributes),
    (Instances.populated_build_file_properties(), BuildFileProperties),
    (BuildFileProperties(), BuildFileProperties),
    (Instances.populated_project_build_file(), ProjectBuildFile),
    (Instances.empty_project_build_file(), ProjectBuildFile),
    (Instances.populated_target_build_file(), TargetBuildFile),
    (Instances.empty_target_build_file(), TargetBuildFile),
    (Instances.populated_project_build_phase_reference(), ProjectBuildPhaseReference),
    (ProjectBuildPhaseReference.of_object_id(Instances.object_id()), ProjectBuildPhaseReference),
    (Instances.populated_target_build_phase_reference(), TargetBuildPhaseReference),
    (TargetBuildPhaseReference.of_object_id(Instances.object_id()), TargetBuildPhaseReference),
    (BuildPhase(BuildPhaseKind.SCRIPT, Instances.populated_script_properties()), BuildPhase),
    (BuildPhase(BuildPhaseKind.COPY, Instances.populated_copy_properties()), BuildPhase),
    (BuildPhase(BuildPhaseKind.APPLE_SCRIPT, Instances.populated_apple_script_properties()), BuildPhase),
    (BuildPhase(BuildPhaseKind.SOURCES, BuildPhaseProperties()), BuildPhase),
    (BuildPhase(BuildPhaseKind.HEADERS, BuildPhaseProperties(Instances.object_id(), "Copy Headers")), BuildPhase),
    (Instances.populated_build_rule(), BuildRule),
    (BuildRule(), BuildRule),
    (Instances.populated_common_exception_set_properties(), CommonExceptionSetProperties),
    (CommonExceptionSetProperties(), CommonExceptionSetProperties),
    (FolderExceptionSet.of_target(Instances.populated_target_exception_set()), FolderExceptionSet),
    (FolderExceptionSet.of_build_phase(Instances.populated_build_phase_exception_set()), FolderExceptionSet),
    (Instances.populated_file_reference(), FileReference),
    (FileReference(), FileReference),
    (Instances.populated_folder(), Folder),
    (Instances.populated_variant_group(), VariantGroup),
    (Instances.populated_version_group(), VersionGroup),
    (Reference.of_file(Instances.populated_file_reference()), Reference),
    (Reference.of_group(Instances.populated_group()), Reference),
    (Reference.of_folder(Instances.populated_folder()), Reference),
    (Reference.of_variant_group(Instances.populated_variant_group()), Reference),
    (Reference.of_version_group(Instances.populated_version_group()), Reference),
    (Instances.populated_swift_package(), SwiftPackage),
    (Instances.empty_swift_package(), SwiftPackage),
    (Instances.populated_remote_product(), RemoteProduct),
    (Instances.populated_remote_target(), RemoteTarget),
    (Instances.populated_package_product_reference(), SwiftPackageProductReference),
    (Instances.populated_package_product_target_member(), SwiftPackageProductTargetMember),
    (TargetDependency.of_local_target(LocalTargetReference("App")), TargetDependency),
    (TargetDependency.of_local_target(LocalTargetReference("App"), frozenset({PlatformFilter("ios")})), TargetDependency),
    (TargetDependency.of_remote_target(Instances.populated_remote_target()), TargetDependency),
    (TargetDependency.of_package(Instances.populated_package_product_reference()), TargetDependency),
    (Configuration(ConfigurationName("Debug")), Configuration),
    (Configuration(ConfigurationName("Debug"), Instances.populated_anchored_reference(), Instances.object_id()), Configuration),
    (Target.native(Instances.populated_common_target_properties()), Target),
    (Target.aggregate(Instances.empty_common_target_properties()), Target),
    (Target.external_build_system(Instances.populated_external_target_properties()), Target),
    (Instances.populated_project(), Project),
    (Instances.empty_project(), Project),
]

VERSION_CONSTRAINTS = [
    SwiftPackageVersionConstraint.revision("1"),
    SwiftPackageVersionConstraint.branch("2"),
    SwiftPackageVersionConstraint.version("3"),
    SwiftPackageVersionConstraint.version_range("4", "5"),
    SwiftPackageVersionConstraint.version_range("a", "b"),
    SwiftPackageVersionConstraint.up_to_next_minor_version("6"),
    SwiftPackageVersionConstraint.up_to_next_major_version("7"),
]
