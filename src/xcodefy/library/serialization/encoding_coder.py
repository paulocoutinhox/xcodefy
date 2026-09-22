from typing import Any, Protocol

from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value


class EncodingCoder(Protocol):
    def open(self, container_type: type, density: PrintingDensity | None) -> Any: ...

    def encode_child(self, value: Any) -> Value: ...

    def note_density(self, path: AbsolutePath, density: PrintingDensity) -> None: ...
