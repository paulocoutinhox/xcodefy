from dataclasses import dataclass

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.field import Field


@dataclass(frozen=True, slots=True)
class FieldOrComment:
    field: Field | None = None
    comment: Comment | None = None

    def __post_init__(self) -> None:
        if (self.field is None) == (self.comment is None):
            raise ValidationError("A field or comment entry must carry exactly one of the two.")

    @property
    def is_field(self) -> bool:
        return self.field is not None
