from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Encodable(Protocol):
    def encode(self, coder: Any) -> None: ...
