from xcodefy.errors.xcodefy_error import XcodefyError


class DecodeError(XcodefyError):
    def __init__(self, message: str, coding_path: str | None = None) -> None:
        located = bool(coding_path)
        super().__init__(f"{message} at {coding_path}" if located else message)
        self.message = message
        self.coding_path = coding_path if located else None
