from __future__ import annotations

from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.encoding_coder import EncodingCoder
from xcodefy.library.serialization.path_component import PathComponent


class EncodingContainer:
    def __init__(self, coder: EncodingCoder, parent: EncodingContainer | None, component: PathComponent | None) -> None:
        self.coder = coder
        self.parent = parent
        self.path = parent.path.appending_component(component) if parent is not None else AbsolutePath()
        self.component_being_encoded: PathComponent | None = None
