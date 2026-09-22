import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCK = re.compile(r"```python\n(.*?)```", re.S)
DOCUMENTS = ["README.md", "docs/getting-started.md", "docs/manipulation.md", "docs/serialization.md"]


class Documentation:
    @staticmethod
    def documents() -> list[Path]:
        return [ROOT / name for name in DOCUMENTS]

    @staticmethod
    def blocks(path: Path) -> list[str]:
        return [block for block in BLOCK.findall(path.read_text(encoding="utf-8"))]
