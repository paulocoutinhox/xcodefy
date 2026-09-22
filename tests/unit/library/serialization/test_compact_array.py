from xcodefy.library.serialization.compact_array import CompactArray


def test_an_empty_compact_array_has_no_values():
    assert CompactArray().values == ()


def test_of_preserves_the_given_order():
    assert CompactArray.of(["b", "a"]).values == ("b", "a")
