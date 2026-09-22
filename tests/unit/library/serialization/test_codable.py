from typing import Any, Self

from xcodefy.library.serialization.codable import Codable
from xcodefy.library.serialization.decodable import Decodable
from xcodefy.library.serialization.encodable import Encodable


class Sample:
    def encode(self, coder: Any) -> None:
        return None

    @classmethod
    def decode(cls, coder: Any) -> Self:
        return cls()


def test_codable_combines_both_halves_of_the_contract():
    assert issubclass(Codable, Encodable)
    assert issubclass(Codable, Decodable)


def test_a_type_with_both_methods_satisfies_the_protocol():
    assert isinstance(Sample(), Codable)
    assert not isinstance(object(), Codable)
