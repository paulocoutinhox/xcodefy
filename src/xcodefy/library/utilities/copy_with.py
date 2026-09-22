from dataclasses import replace
from typing import Any, Self


class CopyWith:
    def copy(self, **changes: Any) -> Self:
        return replace(self, **changes)
