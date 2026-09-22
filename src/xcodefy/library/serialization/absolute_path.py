from __future__ import annotations

from dataclasses import dataclass

from xcodefy.library.serialization.path_component import PathComponent


@dataclass(frozen=True, slots=True)
class AbsolutePath:
    components: tuple[PathComponent, ...] = ()

    def appending_component(self, component: PathComponent) -> AbsolutePath:
        return AbsolutePath((*self.components, component))

    def appending_key(self, key: str) -> AbsolutePath:
        return AbsolutePath((*self.components, PathComponent(key=key)))

    def appending_index(self, index: int) -> AbsolutePath:
        return AbsolutePath((*self.components, PathComponent(index=index)))

    def __str__(self) -> str:
        return "".join(str(component) for component in self.components)
