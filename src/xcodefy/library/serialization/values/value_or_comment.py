from dataclasses import dataclass
from typing import Any

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment import Comment


@dataclass(frozen=True, slots=True)
class ValueOrComment:
    value: Any = None
    comment: Comment | None = None

    def __post_init__(self) -> None:
        if (self.value is None) == (self.comment is None):
            raise ValidationError("A value or comment entry must carry exactly one of the two.")

    @property
    def is_value(self) -> bool:
        return self.value is not None
