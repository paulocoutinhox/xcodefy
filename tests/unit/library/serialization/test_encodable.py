from typing import Any

from xcodefy.library.serialization.encodable import Encodable


class Sample:
    def encode(self, coder: Any) -> None:
        return None


def test_a_type_with_an_encode_method_satisfies_the_protocol():
    assert isinstance(Sample(), Encodable)


def test_a_type_without_an_encode_method_does_not_satisfy_the_protocol():
    assert not isinstance(object(), Encodable)
