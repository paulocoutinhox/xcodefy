from dataclasses import dataclass

from xcodefy.errors.validation_error import ValidationError


@dataclass(frozen=True, slots=True)
class PathComponent:
    key: str | None = None
    index: int | None = None

    def __post_init__(self) -> None:
        if (self.key is None) == (self.index is None):
            raise ValidationError("A path component must carry exactly one locator.")

    def __str__(self) -> str:
        return f"/{self.key}" if self.key is not None else f"[{self.index}]"
