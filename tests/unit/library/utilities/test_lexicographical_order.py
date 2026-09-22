from xcodefy.library.utilities.lexicographical_order import LexicographicalOrder


def test_orders_compare_component_by_component():
    assert LexicographicalOrder(("a", 1)) < LexicographicalOrder(("a", 2))
    assert LexicographicalOrder(("a", 2)) < LexicographicalOrder(("b", 1))
    assert not LexicographicalOrder(("b", 1)) < LexicographicalOrder(("a", 2))


def test_equal_content_compares_equal():
    assert LexicographicalOrder(("a", 1)) == LexicographicalOrder(("a", 1))


def test_orders_sort_a_sequence():
    values = [LexicographicalOrder(("b",)), LexicographicalOrder(("a",))]
    assert sorted(values) == [LexicographicalOrder(("a",)), LexicographicalOrder(("b",))]
