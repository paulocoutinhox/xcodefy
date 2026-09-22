from tests.support.instances import Instances
from tests.support.round_trip import RoundTrip
from xcodefy.library.schema.references.groups.variant_group import VariantGroup
from xcodefy.library.serialization.printing_density import PrintingDensity


def test_a_childless_group_with_at_most_one_build_file_prints_compactly():
    group = VariantGroup()
    assert group.printing_density is PrintingDensity.COMPACT
    group.build_files.append(Instances.populated_project_build_file())
    assert group.printing_density is PrintingDensity.COMPACT
    group.build_files.append(Instances.populated_project_build_file())
    assert group.printing_density is None


def test_children_make_the_group_sprawling():
    group = VariantGroup(children=[Instances.populated_file_reference()])
    assert group.printing_density is None


def test_a_populated_group_round_trips():
    RoundTrip.expect_equal(Instances.populated_variant_group(), VariantGroup)
