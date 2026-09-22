from xcodefy.library.serialization.decoding_coder import DecodingCoder
from xcodefy.library.serialization.values.value import Value


class DecodingContainer:
    def __init__(self, coder: DecodingCoder) -> None:
        self.coder = coder
        self.path = coder.path
        self.value: Value = coder.current
