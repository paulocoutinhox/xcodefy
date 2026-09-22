from typing import Any, Self

from xcodefy.library.serialization.decodable import Decodable


class Sample:
    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls()


def test_a_type_with_a_decode_method_satisfies_the_protocol():
    assert isinstance(Sample(), Decodable)


def test_a_type_without_a_decode_method_does_not_satisfy_the_protocol():
    assert not isinstance(object(), Decodable)
