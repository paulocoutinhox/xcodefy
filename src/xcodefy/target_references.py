from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.project import GROUPED_FILE_KINDS, Project
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.schema.references.reference_kind import ReferenceKind
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.dependencies.remote_product import RemoteProduct
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.dependencies.target_dependency_kind import TargetDependencyKind
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference

BuildFileOwner = FileReference | VariantGroup | VersionGroup | RemoteProduct


class TargetReferences:
    @staticmethod
    def remove(project: Project, target: LocalTargetReference) -> None:
        for file_reference in project.file_references():
            TargetReferences._drop_build_files(file_reference, target)
        for reference in project.references():
            if reference.kind in GROUPED_FILE_KINDS:
                TargetReferences._drop_build_files(reference.content, target)
            elif reference.kind is ReferenceKind.FOLDER:
                TargetReferences._clean_folder(reference.content, target)
        for product in project.imported_products:
            TargetReferences._drop_build_files(product, target)
        for remaining in project.targets:
            TargetReferences._clean_target(remaining.common_properties, target)

    @staticmethod
    def _drop_build_files(owner: BuildFileOwner, target: LocalTargetReference) -> None:
        owner.build_files = [build_file for build_file in owner.build_files if not TargetReferences._maps_into(build_file, target)]

    @staticmethod
    def _maps_into(build_file: ProjectBuildFile, target: LocalTargetReference) -> bool:
        return build_file.build_phase.target == target

    @staticmethod
    def _clean_folder(folder: Folder, target: LocalTargetReference) -> None:
        folder.targets = frozenset(member for member in folder.targets if member != target)
        folder.membership_exceptions = [exception for exception in folder.membership_exceptions if not TargetReferences._names_target(exception, target)]

    @staticmethod
    def _names_target(exception: FolderExceptionSet, target: LocalTargetReference) -> bool:
        if exception.target is not None:
            return exception.target.target == target
        return exception.build_phase.build_phase.target == target

    @staticmethod
    def _clean_target(properties: CommonTargetProperties, target: LocalTargetReference) -> None:
        properties.dependencies = [dependency for dependency in properties.dependencies if not TargetReferences._depends_on(dependency, target)]
        if properties.test_host_target == target:
            properties.test_host_target = None

    @staticmethod
    def _depends_on(dependency: TargetDependency, target: LocalTargetReference) -> bool:
        return dependency.kind is TargetDependencyKind.LOCAL_TARGET and dependency.content == target
