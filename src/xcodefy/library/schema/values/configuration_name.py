from dataclasses import dataclass

from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper


@dataclass(frozen=True, slots=True)
class ConfigurationName(TypedStringWrapper):
    pass
