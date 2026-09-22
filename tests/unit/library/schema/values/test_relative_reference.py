from xcodefy.library.schema.values.relative_reference import RelativeReference


def test_both_relative_references_are_represented():
    assert [member.value for member in RelativeReference] == [".", ".."]
