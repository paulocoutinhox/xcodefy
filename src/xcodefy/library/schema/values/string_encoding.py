from __future__ import annotations

from xcodefy.library.serialization.codable_str_enum import CodableStrEnum


class StringEncoding(CodableStrEnum):
    ASCII = "ascii"
    NEXTSTEP = "nextstep"
    JAPANESE_EUC = "japanese-euc"
    UTF8 = "utf8"
    ISO_LATIN_1 = "iso-latin-1"
    SYMBOL = "symbol"
    NON_LOSSY_ASCII = "non-lossy-ascii"
    SHIFT_JIS = "shift-jis"
    ISO_LATIN_2 = "iso-latin-2"
    UNICODE = "unicode"
    WINDOWS_CP1251 = "windows-code-page-1251"
    WINDOWS_CP1252 = "windows-code-page-1252"
    WINDOWS_CP1253 = "windows-code-page-1253"
    WINDOWS_CP1254 = "windows-code-page-1254"
    WINDOWS_CP1250 = "windows-code-page-1250"
    ISO_2022_JP = "iso-2022-jp"
    MACOS_ROMAN = "macos-roman"
    UTF16 = "utf16"
    UTF16_BIG_ENDIAN = "utf16-big-endian"
    UTF16_LITTLE_ENDIAN = "utf16-little-endian"
    UTF32 = "utf32"
    UTF32_BIG_ENDIAN = "utf32-big-endian"
    UTF32_LITTLE_ENDIAN = "utf32-little-endian"

    @property
    def encoding_value(self) -> int:
        return ENCODING_VALUES[self]

    @staticmethod
    def from_encoding_value(value: int) -> StringEncoding | None:
        return ENCODING_NAMES.get(value)


ENCODING_VALUES = {
    StringEncoding.ASCII: 1,
    StringEncoding.NEXTSTEP: 2,
    StringEncoding.JAPANESE_EUC: 3,
    StringEncoding.UTF8: 4,
    StringEncoding.ISO_LATIN_1: 5,
    StringEncoding.SYMBOL: 6,
    StringEncoding.NON_LOSSY_ASCII: 7,
    StringEncoding.SHIFT_JIS: 8,
    StringEncoding.ISO_LATIN_2: 9,
    StringEncoding.UNICODE: 10,
    StringEncoding.WINDOWS_CP1251: 11,
    StringEncoding.WINDOWS_CP1252: 12,
    StringEncoding.WINDOWS_CP1253: 13,
    StringEncoding.WINDOWS_CP1254: 14,
    StringEncoding.WINDOWS_CP1250: 15,
    StringEncoding.ISO_2022_JP: 21,
    StringEncoding.MACOS_ROMAN: 30,
    StringEncoding.UTF16: 10,
    StringEncoding.UTF16_BIG_ENDIAN: 0x90000100,
    StringEncoding.UTF16_LITTLE_ENDIAN: 0x94000100,
    StringEncoding.UTF32: 0x8C000100,
    StringEncoding.UTF32_BIG_ENDIAN: 0x98000100,
    StringEncoding.UTF32_LITTLE_ENDIAN: 0x9C000100,
}

ENCODING_NAMES = {value: name for name, value in reversed(list(ENCODING_VALUES.items()))}
