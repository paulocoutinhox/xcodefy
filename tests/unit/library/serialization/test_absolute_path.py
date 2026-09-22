from xcodefy.library.serialization.absolute_path import AbsolutePath
from xcodefy.library.serialization.path_component import PathComponent


def test_a_new_path_is_the_root():
    assert AbsolutePath().components == ()
    assert str(AbsolutePath()) == ""


def test_appending_builds_a_readable_path():
    path = AbsolutePath().appending_key("files").appending_index(0).appending_key("name")
    assert str(path) == "/files[0]/name"
    assert len(path.components) == 3


def test_appending_a_component_matches_the_typed_helpers():
    assert AbsolutePath().appending_component(PathComponent(key="a")) == AbsolutePath().appending_key("a")
    assert AbsolutePath().appending_component(PathComponent(index=1)) == AbsolutePath().appending_index(1)


def test_paths_are_hashable_so_they_can_key_the_density_map():
    assert len({AbsolutePath().appending_key("a"), AbsolutePath().appending_key("a")}) == 1
