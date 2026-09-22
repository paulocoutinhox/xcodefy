from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_container import EncodingContainer
from xcodefy.library.serialization.printing_density import PrintingDensity


class Nesting:
    def __init__(self) -> None:
        self.paths: list[str] = []

    def encode(self, coder) -> None:
        container = coder.keyed()
        self.paths.append(str(container.path))
        container.put_unconditionally("child", Nesting() if not self.paths[-1] else [1])


def test_a_root_container_sits_at_the_root_path():
    container = EncodingContainer(Encoder(), None, None)
    assert str(container.path) == ""
    assert container.component_being_encoded is None


def test_a_child_container_extends_the_parent_path():
    outer = Nesting()
    Encoder.json_for(outer)
    assert outer.paths == [""]


def test_a_nested_container_records_the_path_it_was_opened_at():
    encoder = Encoder()
    container = encoder.keyed()
    container.put_unconditionally("names", [1], PrintingDensity.COMPACT)
    assert str(next(iter(encoder.densities))) == "/names"
