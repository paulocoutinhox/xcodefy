from collections.abc import Callable, Iterable
from typing import Any


class Sequences:
    @staticmethod
    def compacted(values: Iterable[Any]) -> list[Any]:
        return [value for value in values if value is not None]

    @staticmethod
    def duplicate_values(values: Iterable[Any], accessor: Callable[[Any], Any]) -> set[Any]:
        seen: set[Any] = set()
        duplicates: set[Any] = set()
        for value in values:
            projected = accessor(value)
            if projected in seen:
                duplicates.add(projected)
            seen.add(projected)
        return duplicates

    @staticmethod
    def sorted_on(values: Iterable[Any], accessor: Callable[[Any], Any]) -> list[Any]:
        return sorted(values, key=accessor)
