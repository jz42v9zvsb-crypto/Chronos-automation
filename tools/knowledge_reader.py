"""
Chronos OS — Knowledge Reader

Reads previously saved research knowledge from knowledge/<project>/ so the
research pipeline can reuse existing findings before doing new research.

Deterministic. No embeddings, no LLM, no vector database.
Mirrors KnowledgeWriter's on-disk layout (knowledge/<sanitized-project>/*.md).
"""

import re
from datetime import datetime
from pathlib import Path


def _sanitize(name: str) -> str:
    """Match KnowledgeWriter's directory sanitization so reads find writes."""
    name = name.strip().lower()
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


class KnowledgeReader:
    def __init__(self, root: Path):
        self.root = Path(root)

    def read_project_knowledge(self, project: str, limit: int = 5) -> list[dict]:
        """
        Return up to `limit` most-recent knowledge files for a project.

        "Most recent" = highest file modification time; ties broken by filename
        (reverse) so ordering is fully deterministic. Returns [] if the project
        knowledge directory does not exist.
        """
        directory = self.root / "knowledge" / _sanitize(project)
        if not directory.exists():
            return []

        files = sorted(
            directory.glob("*.md"),
            key=lambda p: (p.stat().st_mtime, p.name),
            reverse=True,
        )

        items = []
        for path in files[:limit]:
            stat = path.stat()
            items.append({
                "title":       path.stem,
                "filename":    path.name,
                "path":        str(path),
                "content":     path.read_text(encoding="utf-8"),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
        return items

    def to_markdown(self, knowledge_items: list[dict]) -> str:
        """Render existing knowledge as a markdown block for the prompt context."""
        if not knowledge_items:
            return ""

        sections = ["# EXISTING KNOWLEDGE"]
        for item in knowledge_items:
            sections.append(f"## {item['title']} ({item['modified_at']})\n\n{item['content']}")
        return "\n\n---\n\n".join(sections)
