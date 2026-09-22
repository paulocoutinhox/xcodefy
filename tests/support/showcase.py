from pathlib import Path

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
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.folder.exception_sets.common_exception_set_properties import CommonExceptionSetProperties
from xcodefy.library.schema.references.folder.exception_sets.exception_set_sense import ExceptionSetSense
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.target_exception_set import TargetExceptionSet
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.external_build_system_target_properties import ExternalBuildSystemTargetProperties
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.build_setting import BuildSetting
from xcodefy.library.schema.values.bundle_base_path import BundleBasePath
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.file_type_id import FileTypeID
from xcodefy.library.schema.values.folder_member_id import FolderMemberID
from xcodefy.library.schema.values.group_tree_reference import GroupTreeReference
from xcodefy.library.schema.values.language import Language
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.product_type_id import ProductTypeID
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo
from xcodefy.xcode_project import XcodeProject

PLATFORMS = {
    "iphoneos": ("IPHONEOS_DEPLOYMENT_TARGET", "18.0"),
    "macosx": ("MACOSX_DEPLOYMENT_TARGET", "15.0"),
    "watchos": ("WATCHOS_DEPLOYMENT_TARGET", "11.0"),
    "appletvos": ("TVOS_DEPLOYMENT_TARGET", "18.0"),
    "xros": ("XROS_DEPLOYMENT_TARGET", "2.0"),
    "driverkit.macosx": ("DRIVERKIT_DEPLOYMENT_TARGET", "24.0"),
}

PRODUCT_TYPES = {
    "App": ("application", "iphoneos"),
    "AppClip": ("application.on-demand-install-capable", "iphoneos"),
    "WatchApp": ("application.watchapp2", "watchos"),
    "MacApp": ("application", "macosx"),
    "TVApp": ("application", "appletvos"),
    "VisionApp": ("application", "xros"),
    "NotificationService": ("app-extension", "iphoneos"),
    "WidgetExtension": ("extensionkit-extension", "iphoneos"),
    "Shared": ("framework", "iphoneos"),
    "SharedStatic": ("framework.static", "macosx"),
    "DynamicLibrary": ("library.dynamic", "macosx"),
    "StaticLibrary": ("library.static", "macosx"),
    "ResourceBundle": ("bundle", "macosx"),
    "CommandLineTool": ("tool", "macosx"),
    "XPCService": ("xpc-service", "macosx"),
    "SystemExtension": ("system-extension", "macosx"),
    "DriverExtension": ("driver-extension", "driverkit.macosx"),
    "AppTests": ("bundle.unit-test", "iphoneos"),
    "AppUITests": ("bundle.ui-testing", "iphoneos"),
}

SWIFT_SOURCES = {
    "Shared/Calculator.swift": "public struct Calculator {\n    public init() {}\n\n    public func add(_ first: Int, _ second: Int) -> Int {\n        first + second\n    }\n}\n",
    "App/AppMain.swift": "import Shared\n\n@main\nstruct AppMain {\n    static func main() {\n        print(Calculator().add(2, 3))\n    }\n}\n",
    "AppTests/CalculatorTests.swift": "import XCTest\n\n@testable import Shared\n\nfinal class CalculatorTests: XCTestCase {\n    func testAddition() {\n        XCTAssertEqual(Calculator().add(2, 3), 5)\n    }\n}\n",
}

RESOURCES = {"App/en.lproj/Main.strings": '"greeting" = "Hello";\n', "App/Model.xcdatamodeld/Model.xcdatamodel": "<model/>\n", "Generated/Legacy.swift": "// discovered from disk\n", "Generated/Public.h": "// header\n"}


class Showcase:
    @staticmethod
    def settings(sdk: str) -> dict[str, BuildSetting]:
        key, value = PLATFORMS[sdk]
        return {"SDKROOT": BuildSetting.of_string(sdk), key: BuildSetting.of_string(value), "SUPPORTED_PLATFORMS": BuildSetting.of_array([sdk])}

    @staticmethod
    def phases(name: str) -> list[BuildPhase]:
        script = ScriptBuildPhaseProperties(BuildPhaseProperties(None, "Lint"), "/bin/sh", "swiftlint\nexit 0", scope=BuildPhaseScope.ALWAYS)
        copy = CopyFilesBuildPhaseProperties(BuildPhaseProperties(None, "Embed"), BundleBasePath.PLUG_INS_DIR, "", BuildPhaseScope.INSTALL)
        common = [BuildPhase.of_kind(BuildPhaseKind.SOURCES), BuildPhase.of_kind(BuildPhaseKind.RESOURCES), BuildPhase.of_kind(BuildPhaseKind.FRAMEWORKS)]
        if name != "App":
            return common
        apple_script = AppleScriptBuildPhaseProperties(BuildPhaseProperties(None, "Run AppleScript"), True, "Context")
        extra = [BuildPhase.of_kind(BuildPhaseKind.HEADERS), BuildPhase.of_kind(BuildPhaseKind.REZ), BuildPhase.of_kind(BuildPhaseKind.JAVA_ARCHIVE)]
        return [*common, *extra, BuildPhase(BuildPhaseKind.COPY, copy), BuildPhase(BuildPhaseKind.SCRIPT, script), BuildPhase(BuildPhaseKind.APPLE_SCRIPT, apple_script)]

    @staticmethod
    def native_targets() -> list[Target]:
        targets = []
        for name, (product_type, sdk) in PRODUCT_TYPES.items():
            dependencies = [TargetDependency.of_local_target(LocalTargetReference("Shared"))] if name == "App" else []
            rules = [BuildRule("com.apple.compilers.proxy.script", "Recompress", FileTypeID("image.png"), script="echo recompress")] if name == "App" else []
            configurations = [Configuration(ConfigurationName("Debug"), object_id=ObjectID(f"{name}-DEBUG"))] if name == "App" else []
            properties = CommonTargetProperties(
                name,
                ObjectID(name.upper()),
                build_phases=Showcase.phases(name),
                build_settings=Showcase.settings(sdk),
                product_type_id=ProductTypeID.from_abbreviated(product_type),
                product=GroupTreeReference.of_child_names(["Products", name]),
                dependencies=dependencies,
                build_rules=rules,
                specialized_configurations=configurations,
            )
            targets.append(Target.native(properties))
        return targets

    @staticmethod
    def other_targets() -> list[Target]:
        aggregate = CommonTargetProperties("Everything", ObjectID("EVERYTHING"), dependencies=[TargetDependency.of_local_target(LocalTargetReference(name)) for name in PRODUCT_TYPES])
        external = CommonTargetProperties("Docs", ObjectID("DOCS"))
        return [Target.aggregate(aggregate), Target.external_build_system(ExternalBuildSystemTargetProperties(external, "/usr/bin/make", "docs", "$(SRCROOT)", False))]

    @staticmethod
    def discovered_folder() -> Reference:
        member = FolderMemberID("Legacy.swift")
        common = CommonExceptionSetProperties(ExceptionSetSense.EXCLUSIONS, frozenset({member}))
        exception = FolderExceptionSet.of_target(TargetExceptionSet(LocalTargetReference("App"), frozenset({FolderMemberID("Public.h")}), frozenset(), {}, common))
        folder = Folder(FilePath.from_string_representation("Generated"), targets=frozenset({LocalTargetReference("App")}), membership_exceptions=[exception])
        return Reference.of_folder(folder)

    @staticmethod
    def localized_group() -> Reference:
        child = FileReference(FilePath.from_string_representation("App/en.lproj/Main.strings"))
        return Reference.of_variant_group(VariantGroup(FilePath(), "Main.strings", children=[child]))

    @staticmethod
    def versioned_group() -> Reference:
        child = FileReference(FilePath.from_string_representation("Model.xcdatamodel"))
        current = GroupTreeReference.of_child_names(["Model.xcdatamodel"])
        return Reference.of_version_group(VersionGroup(FilePath.from_string_representation("App/Model.xcdatamodeld"), "Model.xcdatamodeld", current_version=current, versioned_file_type=FileTypeID("wrapper.xcdatamodel"), children=[child]))

    @staticmethod
    def packages() -> list[SwiftPackage]:
        constraint = SwiftPackageVersionConstraint.up_to_next_major_version("1.4.0")
        remote = RemoteSwiftPackage("https://github.com/apple/swift-collections.git", constraint)
        return [SwiftPackage(SwiftPackageLocation.of_local(LocalSwiftPackage("../SharedPackage"))), SwiftPackage(SwiftPackageLocation.of_remote(remote), ["Traits"])]

    @staticmethod
    def project() -> XcodeProject:
        configurations = [Configuration(ConfigurationName("Debug")), Configuration(ConfigurationName("Release"))]
        localization = ProjectLocalizationInfo(Language("en"), frozenset({Language("pt-BR")}))
        settings = {"SWIFT_VERSION": BuildSetting.of_string("6.0"), "ENABLE_USER_SCRIPT_SANDBOXING": BuildSetting.of_string("YES")}
        project = Project([], ConfigurationName("Debug"), localization, packages=Showcase.packages(), configurations=configurations, build_settings=settings, targets=[*Showcase.native_targets(), *Showcase.other_targets()], organization_name="Example", class_prefix="EX")
        wrapper = XcodeProject(project)
        for group in sorted({Path(name).parts[0] for name in SWIFT_SOURCES}):
            wrapper.add_group(group)
        for name in SWIFT_SOURCES:
            group, file_name = Path(name).parts[0], Path(name).name
            wrapper.add_file(file_name, target=group, group=group)
        project.top_level_references.extend([Showcase.discovered_folder(), Showcase.localized_group(), Showcase.versioned_group()])
        return wrapper

    @staticmethod
    def write(directory: Path) -> Path:
        for name, content in {**SWIFT_SOURCES, **RESOURCES}.items():
            target = directory / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return Showcase.project().save(directory / "Showcase.xcodeproj")
