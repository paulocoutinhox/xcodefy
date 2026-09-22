from typing import Protocol, runtime_checkable

from xcodefy.library.serialization.decodable import Decodable
from xcodefy.library.serialization.encodable import Encodable


@runtime_checkable
class Codable(Encodable, Decodable, Protocol):
    pass
