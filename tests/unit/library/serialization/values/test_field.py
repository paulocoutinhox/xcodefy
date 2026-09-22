from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.value import Value


def test_a_field_pairs_a_key_with_a_value():
    field = Field("key", Value.string("value"))
    assert (field.key, field.value) == ("key", Value.string("value"))
