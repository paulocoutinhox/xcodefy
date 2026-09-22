from dataclasses import dataclass

from xcodefy.errors.validation_error import ValidationError
from xcodefy.library.serialization.values.comment_style import CommentStyle
from xcodefy.library.utilities.text import Text


@dataclass(frozen=True, slots=True)
class Comment:
    style: CommentStyle
    content: str

    def __post_init__(self) -> None:
        if self.style is CommentStyle.BLOCK and ("/*" in self.content or "*/" in self.content):
            raise ValidationError("Comment contains internal terminators.")

    @property
    def allows_compact_printing(self) -> bool:
        return self.style is CommentStyle.BLOCK and not Text.has_json_line_separator(self.content)
