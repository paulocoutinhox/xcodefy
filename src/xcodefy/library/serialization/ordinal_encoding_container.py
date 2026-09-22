from __future__ import annotations

from typing import Any

from xcodefy.library.serialization.encoding_coder import EncodingCoder
from xcodefy.library.serialization.encoding_container import EncodingContainer
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_or_comment import ValueOrComment


class OrdinalEncodingContainer(EncodingContainer):
    def __init__(self, coder: EncodingCoder, parent: EncodingContainer | None, component: PathComponent | None) -> None:
        super().__init__(coder, parent, component)
        self.entries: list[ValueOrComment] = []

    def put(self, value: Any, density: PrintingDensity | None = None) -> None:
        index = len(self.entries)
        self.component_being_encoded = PathComponent(index=index)
        encoded = self.coder.encode_child(value)
        self.component_being_encoded = None
        self.entries.append(ValueOrComment(value=encoded))
        if density is not None:
            self.coder.note_density(self.path.appending_index(index), density)

    def add_comment(self, comment: Comment) -> None:
        self.entries.append(ValueOrComment(comment=comment))

    def finish(self) -> Value:
        return Value.array(self.entries)
