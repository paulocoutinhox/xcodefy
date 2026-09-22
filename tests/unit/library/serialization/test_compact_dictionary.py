from xcodefy.library.serialization.compact_dictionary import CompactDictionary


def test_an_empty_compact_dictionary_has_no_values():
    assert CompactDictionary().values == {}


def test_of_wraps_the_given_mapping():
    assert CompactDictionary.of({"a": 1}).values == {"a": 1}


def test_equality_compares_the_wrapped_mapping():
    assert CompactDictionary.of({"a": 1}) == CompactDictionary.of({"a": 1})
