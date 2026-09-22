from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from xcodefy.library.serialization.decoders import Decoders
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(frozen=True, slots=True)
class MultilineText:
    text: str = ""

    @property
    def lines(self) -> list[str]:
        return self.text.split("\n")

    @property
    def encodes_to_string(self) -> bool:
        lines = self.lines
        return len(lines) == 1 or (len(lines) == 2 and lines[1] == "")

    def encode(self, coder: Any) -> None:
        if self.encodes_to_string:
            coder.encode_string(self.text)
            return
        container = coder.ordinal()
        for line in self.lines:
            container.put(line)

    @classmethod
    def decode(cls, coder: Any) -> Self:
        if coder.current_node_type is ValueType.STRING:
            return cls(coder.decode_string())
        return cls("\n".join(Decoders.array_of(Decoders.string)(coder)))
