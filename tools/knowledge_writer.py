"""
Chronos OS — Knowledge Writer
"""

import re
from pathlib import Path


def _sanitize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


class KnowledgeWriter:
    def __init__(self, root: Path):
        self.root = root

    def save(self, category: str, topic: str, content: str) -> Path:
        # category may be a nested path ("project/strategy"); sanitize each segment
        category = "/".join(_sanitize(part) for part in category.split("/") if part.strip())
        topic = _sanitize(topic)

        directory = self.root / "knowledge" / category
        directory.mkdir(parents=True, exist_ok=True)

        path = directory / f"{topic}.md"
        path.write_text(content, encoding="utf-8")
        return path
