from xcodefy.library.serialization.printing_density import PrintingDensity


def test_compact_is_the_only_marker_a_node_can_carry():
    assert [member.value for member in PrintingDensity] == ["compact"]
