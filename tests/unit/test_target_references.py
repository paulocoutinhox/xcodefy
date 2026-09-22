import pytest

from tests.support.instances import Instances
from xcodefy.library.schema.build_files.project_build_file import ProjectBuildFile
from xcodefy.library.schema.build_phase_references.project_build_phase_reference import ProjectBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.project import Project
from xcodefy.library.schema.references.file.file_reference import FileReference
from xcodefy.library.schema.references.folder.exception_sets.build_phase_exception_set import BuildPhaseExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.folder_exception_set import FolderExceptionSet
from xcodefy.library.schema.references.folder.exception_sets.target_exception_set import TargetExceptionSet
from xcodefy.library.schema.references.folder.folder import Folder
from xcodefy.library.schema.references.groups.group import Group
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.schema.references.groups.version_group import VersionGroup
from xcodefy.library.schema.references.reference import Reference
from xcodefy.library.schema.target.common_target_properties import CommonTargetProperties
from xcodefy.library.schema.target.dependencies.target_dependency import TargetDependency
from xcodefy.library.schema.target.target import Target
from xcodefy.library.schema.values.configuration_name import ConfigurationName
from xcodefy.library.schema.values.file_path import FilePath
from xcodefy.library.schema.values.language import Language
from xcodefy.library.schema.values.local_target_reference import LocalTargetReference
from xcodefy.library.schema.values.object_id import ObjectID
from xcodefy.library.schema.values.project_localization_info import ProjectLocalizationInfo
from xcodefy.target_references import TargetReferences

DOOMED = LocalTargetReference("Doomed")
KEPT = LocalTargetReference("Kept")


def path(name):
    return FilePath.from_string_representation(name)


def build_file(target, kind=BuildPhaseKind.SOURCES):
    return ProjectBuildFile(ProjectBuildPhaseReference.named(target, kind))


def object_id_build_file():
    return ProjectBuildFile(ProjectBuildPhaseReference.of_object_id(ObjectID("PHASE")))


def project_with(references, targets):
    return Project(references, ConfigurationName("Debug"), ProjectLocalizationInfo(Language("en")), targets=targets)


def test_build_files_of_a_file_reference_are_dropped():
    reference = FileReference(path("a.swift"), build_files=[build_file(DOOMED), build_file(KEPT)])
    project = project_with([Reference.of_file(reference)], [])
    TargetReferences.remove(project, DOOMED)
    assert [str(entry.build_phase) for entry in reference.build_files] == ["Kept/compile-sources"]


@pytest.mark.parametrize(("group_type", "wrap"), [(VariantGroup, Reference.of_variant_group), (VersionGroup, Reference.of_version_group)])
def test_build_files_of_a_grouped_file_and_of_its_children_are_dropped(group_type, wrap):
    child = FileReference(path("child.swift"), build_files=[build_file(DOOMED), build_file(KEPT)])
    group = group_type(path("G"), "G", build_files=[build_file(DOOMED)], children=[child])
    project = project_with([wrap(group)], [])
    TargetReferences.remove(project, DOOMED)
    assert group.build_files == []
    assert [str(entry.build_phase) for entry in child.build_files] == ["Kept/compile-sources"]


def test_build_files_of_an_imported_product_are_dropped():
    product = Instances.populated_remote_product()
    product.build_files = [build_file(DOOMED), build_file(KEPT)]
    project = project_with([], [])
    project.imported_products = [product]
    TargetReferences.remove(project, DOOMED)
    assert [str(entry.build_phase) for entry in product.build_files] == ["Kept/compile-sources"]


def test_an_object_id_build_phase_reference_is_left_alone():
    reference = FileReference(path("a.swift"), build_files=[object_id_build_file()])
    project = project_with([Reference.of_file(reference)], [])
    TargetReferences.remove(project, DOOMED)
    assert len(reference.build_files) == 1


def test_a_folder_loses_the_target_from_its_membership():
    folder = Folder(path("Src"), targets=frozenset({DOOMED, KEPT}))
    project = project_with([Reference.of_folder(folder)], [])
    TargetReferences.remove(project, DOOMED)
    assert folder.targets == frozenset({KEPT})


def test_a_folder_loses_the_exception_sets_that_named_the_target():
    doomed_target_set = FolderExceptionSet.of_target(TargetExceptionSet(DOOMED))
    kept_target_set = FolderExceptionSet.of_target(TargetExceptionSet(KEPT))
    doomed_phase_set = FolderExceptionSet.of_build_phase(BuildPhaseExceptionSet(ProjectBuildPhaseReference.named(DOOMED, BuildPhaseKind.COPY)))
    kept_phase_set = FolderExceptionSet.of_build_phase(BuildPhaseExceptionSet(ProjectBuildPhaseReference.named(KEPT, BuildPhaseKind.COPY)))
    folder = Folder(path("Src"), membership_exceptions=[doomed_target_set, kept_target_set, doomed_phase_set, kept_phase_set])
    project = project_with([Reference.of_folder(folder)], [])
    TargetReferences.remove(project, DOOMED)
    assert folder.membership_exceptions == [kept_target_set, kept_phase_set]


def test_other_targets_lose_their_dependency_and_test_host():
    dependencies = [TargetDependency.of_local_target(DOOMED), TargetDependency.of_local_target(KEPT)]
    properties = CommonTargetProperties("Tests", ObjectID("T"), dependencies=dependencies, test_host_target=DOOMED)
    project = project_with([], [Target.native(properties)])
    TargetReferences.remove(project, DOOMED)
    assert [dependency.content for dependency in properties.dependencies] == [KEPT]
    assert properties.test_host_target is None


def test_a_test_host_pointing_elsewhere_is_kept():
    properties = CommonTargetProperties("Tests", ObjectID("T"), test_host_target=KEPT)
    project = project_with([], [Target.native(properties)])
    TargetReferences.remove(project, DOOMED)
    assert properties.test_host_target == KEPT


def test_a_nested_group_child_is_reached():
    reference = FileReference(path("a.swift"), build_files=[build_file(DOOMED)])
    group = Group(path("G"), "G", children=[Reference.of_file(reference)])
    project = project_with([Reference.of_group(group)], [])
    TargetReferences.remove(project, DOOMED)
    assert reference.build_files == []
