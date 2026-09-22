from collections.abc import Sequence

from xcodefy.errors.decode_error import DecodeError
from xcodefy.library.utilities.unescape_result import UnescapeResult
from xcodefy.library.utilities.unescape_status import UnescapeStatus

ESCAPE_INDICATOR = "\\"
JSON_LINE_SEPARATORS = frozenset({"\n", "\r", " ", " "})


class Text:
    @staticmethod
    def smart_quoted(value: str) -> str:
        return f"“{value}”"

    @staticmethod
    def quoted(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def has_json_line_separator(value: str) -> bool:
        return any(character in JSON_LINE_SEPARATORS for character in value)

    @staticmethod
    def is_spear_case(value: str) -> bool:
        if not value or not Text.is_lowercase_ascii(value[0]):
            return False
        return all(Text.is_lowercase_ascii(character) or character == "-" for character in value)

    @staticmethod
    def is_lowercase_ascii(character: str) -> bool:
        return character.isascii() and character.islower()

    @staticmethod
    def dropping_required_prefix(value: str, prefix: str) -> str | None:
        return value[len(prefix) :] if value.startswith(prefix) else None

    @staticmethod
    def partition_at_only(value: str, separator: str) -> tuple[str, str] | None:
        if value.count(separator) != 1:
            return None
        index = value.index(separator)
        return value[:index], value[index + len(separator) :]

    @staticmethod
    def joined_with_final_separator(values: Sequence[str], separator: str, final_separator: str) -> str:
        if len(values) <= 1:
            return separator.join(values)
        return separator.join(values[:-1]) + final_separator + values[-1]

    @staticmethod
    def escaping(value: str, escaped_character: str) -> str:
        parts: list[str] = []
        for character in value:
            if character in {escaped_character, ESCAPE_INDICATOR}:
                parts.append(ESCAPE_INDICATOR)
            parts.append(character)
        return "".join(parts)

    @staticmethod
    def unescaping(value: str, escaped_character: str) -> str:
        result = Text.unescaping_until_error(value, escaped_character)
        if result.status == UnescapeStatus.COMPLETE:
            return result.unescaped
        if result.status == UnescapeStatus.UNESCAPED_SEQUENCE:
            quoted_character = Text.smart_quoted(escaped_character)
            raise DecodeError(f"Missing escape sequence for {quoted_character} in {Text.smart_quoted(value)}.")
        if result.status == UnescapeStatus.INVALID_ESCAPE_SEQUENCE:
            quoted_sequence = Text.smart_quoted(ESCAPE_INDICATOR + result.character)
            raise DecodeError(f"Invalid escape sequence {quoted_sequence} in {Text.smart_quoted(value)}.")
        raise DecodeError(f"Invalid escape sequence in {Text.smart_quoted(value)}.")

    @staticmethod
    def unescaping_until_error(value: str, escaped_character: str) -> UnescapeResult:
        if not any(character in {ESCAPE_INDICATOR, escaped_character} for character in value):
            return UnescapeResult(UnescapeStatus.COMPLETE, unescaped=value)
        parts: list[str] = []
        index = 0
        while index < len(value):
            character = value[index]
            if character == ESCAPE_INDICATOR:
                index += 1
                if index == len(value):
                    return UnescapeResult(UnescapeStatus.UNRESOLVED_ESCAPE)
                following = value[index]
                if following not in {escaped_character, ESCAPE_INDICATOR}:
                    return UnescapeResult(UnescapeStatus.INVALID_ESCAPE_SEQUENCE, character=following)
                parts.append(following)
            elif character == escaped_character:
                return UnescapeResult(UnescapeStatus.UNESCAPED_SEQUENCE, unescaped="".join(parts), remaining=value[index + 1 :])
            else:
                parts.append(character)
            index += 1
        return UnescapeResult(UnescapeStatus.COMPLETE, unescaped="".join(parts))
