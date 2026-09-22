from dataclasses import dataclass, field

from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.printing_density import PrintingDensity
from xcodefy.library.serialization.values.value import Value
from xcodefy.library.serialization.values.value_type import ValueType


@dataclass(slots=True)
class DensityValidator:
    densities: dict[AbsolutePath, PrintingDensity] = field(default_factory=dict)

    # A compact request cannot survive a descendant that must span lines, so one pass erases the
    # contradictory requests up front rather than rescanning the tree for every candidate node.
    def validated(self, root: Value) -> dict[AbsolutePath, PrintingDensity]:
        self._validate(root, AbsolutePath())
        return self.densities

    def _validate(self, value: Value, path: AbsolutePath) -> bool:
        allows_compactness = self._validate_children(value, path)
        if self.densities.get(path) is PrintingDensity.COMPACT and not allows_compactness:
            del self.densities[path]
        return allows_compactness

    def _validate_children(self, value: Value, path: AbsolutePath) -> bool:
        if value.type is ValueType.ARRAY:
            return self._validate_array(value, path)
        if value.type is ValueType.OBJECT:
            return self._validate_object(value, path)
        return True

    def _validate_array(self, value: Value, path: AbsolutePath) -> bool:
        allows_compactness = True
        value_index = 0
        for entry in value.content:
            if entry.is_value:
                allows_compactness &= self._validate(entry.value, path.appending_index(value_index))
                value_index += 1
            else:
                allows_compactness &= entry.comment.allows_compact_printing
        return allows_compactness

    def _validate_object(self, value: Value, path: AbsolutePath) -> bool:
        allows_compactness = True
        for entry in value.content.fields_or_comments:
            if entry.is_field:
                allows_compactness &= self._validate(entry.field.value, path.appending_key(entry.field.key))
            else:
                allows_compactness &= entry.comment.allows_compact_printing
        return allows_compactness
