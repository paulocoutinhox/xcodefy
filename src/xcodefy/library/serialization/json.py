from pathlib import Path
from typing import Any

from xcodefy.library.serialization.encoder import Encoder
from xcodefy.library.serialization.encoding_options import EncodingOptions
from xcodefy.library.serialization.parser import Parser
from xcodefy.library.serialization.printer import Printer
from xcodefy.library.serialization.values.value import Value


class JSON:
    @staticmethod
    def parse(text: str) -> Value:
        return Parser(text).parse()

    @staticmethod
    def loads(text: str) -> Any:
        return JSON.parse(text).to_python()

    @staticmethod
    def dumps(value: Any, options: EncodingOptions | None = None) -> str:
        root = value if isinstance(value, Value) else Value.from_python(value)
        return Printer(options=options or EncodingOptions.default()).print(root)

    @staticmethod
    def load(path: str | Path) -> Any:
        return JSON.loads(Path(path).read_text(encoding="utf-8"))

    @staticmethod
    def dump(value: Any, path: str | Path) -> None:
        Path(path).write_text(JSON.dumps(value), encoding="utf-8")

    @staticmethod
    def encode(value: Any, options: EncodingOptions | None = None) -> str:
        return Encoder.text_for(value, options or EncodingOptions.default())
