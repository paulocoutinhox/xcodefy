from __future__ import annotations

from typing import Any

from xcodefy.errors.encode_error import EncodeError
from xcodefy.library.serialization.encoding_coder import EncodingCoder
from xcodefy.library.serialization.encoding_container import EncodingContainer
from xcodefy.library.serialization.path_component import PathComponent
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.comment import Comment
from xcodefy.library.serialization.values.field import Field
from xcodefy.library.serialization.values.field_or_comment import FieldOrComment
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.utilities.text import Text


class KeyedEncodingContainer(EncodingContainer):
    def __init__(self, coder: EncodingCoder, parent: EncodingContainer | None, component: PathComponent | None) -> None:
        super().__init__(coder, parent, component)
        self.entries: list[FieldOrComment] = []
        self.keys: set[str] = set()

    def put_unverified(self, key: str, value: Any, density: PrintingDensity | None = None) -> None:
        if key in self.keys:
            raise EncodeError(f"Encoded the key {Text.smart_quoted(key)} multiple times.")
        self.keys.add(key)
        self.component_being_encoded = PathComponent(key=key)
        if density is not None:
            self.coder.note_density(self.path.appending_key(key), density)
        encoded = self.coder.encode_child(value)
        self.component_being_encoded = None
        self.entries.append(FieldOrComment(field=Field(key, encoded)))

    def put_unconditionally(self, key: str, value: Any, density: PrintingDensity | None = None) -> None:
        if not Text.is_spear_case(key):
            raise EncodeError(f"The key {Text.smart_quoted(key)} is not spear case.")
        self.put_unverified(key, value, density)

    def put(self, key: str, value: Any, default: Any, density: PrintingDensity | None = None) -> None:
        if value != default:
            self.put_unconditionally(key, value, density)

    def put_inline(self, value: Any) -> None:
        if value is not None:
            value.encode_inline(self)

    def add_comment(self, comment: Comment) -> None:
        self.entries.append(FieldOrComment(comment=comment))

    def finish(self) -> Value:
        return Value.object(self.entries)
