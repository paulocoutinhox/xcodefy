from typing import Any, Self


class InlineKeyedCodable:
    __slots__ = ()

    def encode(self, coder: Any) -> None:
        self.encode_inline(coder.keyed())

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls.decode_inline(coder.keyed())
