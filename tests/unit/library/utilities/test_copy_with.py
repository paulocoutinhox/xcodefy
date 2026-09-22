from dataclasses import dataclass

from xcodefy.library.utilities.copy_with import CopyWith


@dataclass(slots=True)
class Sample(CopyWith):
    first: int = 0
    second: str = ""


def test_copy_replaces_only_the_named_fields():
    original = Sample(1, "a")
    copied = original.copy(second="b")
    assert copied == Sample(1, "b")
    assert original == Sample(1, "a")
