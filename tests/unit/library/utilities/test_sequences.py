from xcodefy.library.utilities.sequences import Sequences


def test_compacted_drops_missing_values():
    assert Sequences.compacted([1, None, 2]) == [1, 2]


def test_duplicate_values_reports_repeated_projections():
    assert Sequences.duplicate_values(["aa", "ab", "ba"], lambda value: value[0]) == {"a"}
    assert Sequences.duplicate_values(["a", "b"], lambda value: value) == set()


def test_sorted_on_orders_by_the_projection():
    assert Sequences.sorted_on(["bb", "a"], len) == ["a", "bb"]
