from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.build_files.target_build_file import TargetBuildFile
from xcodefy.library.schema.build_phase_references.target_build_phase_reference import TargetBuildPhaseReference
from xcodefy.library.schema.build_phases.build_phase_kind import BuildPhaseKind
from xcodefy.library.schema.target.dependencies.swift_package_product_reference import SwiftPackageProductReference
from xcodefy.library.schema.target.dependencies.swift_package_product_target_member import SwiftPackageProductTargetMember
from xcodefy.library.schema.values.object_id import ObjectID


def named_member(name=None):
    build_file = TargetBuildFile(TargetBuildPhaseReference.named(BuildPhaseKind.FRAMEWORKS, name))
    return SwiftPackageProductTargetMember(SwiftPackageProductReference("helper"), build_file)


def test_the_package_product_is_written_inline_beside_the_build_phase():
    assert RoundTrip.text(named_member()) == '{\n  "product-name": "helper",\n  "build-phase": { "build-phase": "frameworks" },\n}\n'


def test_a_named_phase_sorts_by_kind_and_name():
    assert named_member("Extra").encoding_order.content[1] == ("frameworks", "Extra", "")


def test_an_unnamed_phase_sorts_with_an_empty_name():
    assert named_member().encoding_order.content[1] == ("frameworks", "", "")


def test_an_object_id_phase_sorts_by_its_identifier():
    build_file = TargetBuildFile(TargetBuildPhaseReference.of_object_id(ObjectID("A1")))
    member = SwiftPackageProductTargetMember(SwiftPackageProductReference("helper"), build_file)
    assert member.encoding_order.content[1] == ("", "", "A1")


def test_a_populated_member_round_trips():
    RoundTrip.expect_equal(Instances.populated_package_product_target_member(), SwiftPackageProductTargetMember)
