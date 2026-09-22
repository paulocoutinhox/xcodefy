from xcodefy.library.serialization.values.value_type import ValueType


def test_every_json_shape_is_represented():
    assert [member.value for member in ValueType] == ["null", "boolean", "integer", "double", "string", "array", "object"]


def test_the_object_type_reports_as_a_dictionary_in_error_messages():
    assert ValueType.OBJECT.error_message_name == "dictionary"
    assert ValueType.STRING.error_message_name == "string"
