from enum import StrEnum


class ValueType(StrEnum):
    NULL = "null"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DOUBLE = "double"
    STRING = "string"
    ARRAY = "array"
    OBJECT = "object"

    @property
    def error_message_name(self) -> str:
        return "dictionary" if self is ValueType.OBJECT else self.value
