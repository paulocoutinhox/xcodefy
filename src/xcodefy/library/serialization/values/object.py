from dataclasses import dataclass, field

from xcodefy.library.serialization.values.field_or_comment import FieldOrComment


@dataclass(slots=True)
class Object:
    fields_or_comments: list[FieldOrComment] = field(default_factory=list)

    @property
    def fields(self) -> list[FieldOrComment]:
        return [entry for entry in self.fields_or_comments if entry.is_field]
