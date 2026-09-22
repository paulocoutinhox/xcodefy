from typing import Any, Protocol, Self, runtime_checkable


@runtime_checkable
class Decodable(Protocol):
    @classmethod
    def decode(cls, coder: Any) -> Self: ...
