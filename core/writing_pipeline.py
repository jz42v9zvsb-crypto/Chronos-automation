"""
Chronos OS — Writing Pipeline

Apollo's flow: read Athena strategy outputs (knowledge/<project>/strategy/) →
build Apollo prompt → LLM → save the deck draft under knowledge/<project>/drafts/.

No web search, no Tavily, no new facts. Apollo writes from the saved strategy.

Note: KnowledgeReader reads only the top-level knowledge/<project>/ directory and
cannot reach the strategy/ subdirectory, so the strategy files are read directly
here (mirroring the reader's on-disk convention) and rendered via the reader's
to_markdown(). KnowledgeReader is left unchanged.
"""

import re
from datetime import datetime
from pathlib import Path

from core.prompt import Prompt


def _topic_slug(task: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    slug = re.sub(r"[^\w]", "_", task[:40].strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return f"{date}_{slug}"


def _sanitize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^\w\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


class WritingPipeline:
    def __init__(self, chronos, llm_client, knowledge_reader):
        self.chronos          = chronos
        self.llm_client       = llm_client
        self.knowledge_reader = knowledge_reader

    def _read_strategy(self, project: str, limit: int = 5) -> list:
        """Read knowledge/<project>/strategy/*.md, most-recent first (deterministic)."""
        base = Path(self.knowledge_reader.root) / "knowledge" / _sanitize(project) / "strategy"
        if not base.exists():
            return []

        files = sorted(
            base.glob("*.md"),
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

    def run(self, project: str, task: str, apollo, knowledge_writer) -> dict:
        # 1. Read Athena strategy outputs (no web search, no new facts)
        items          = self._read_strategy(project)
        source_summary = self.knowledge_reader.to_markdown(items)
        print(f"  [writing] {len(items)} strategy file(s) loaded")

        # 2. Build Apollo prompt grounded in the strategy/handoff
        system = apollo.build_system_prompt(
            context=f"현재 작업은 '{project}' 프로젝트의 STP 장표 초안 작성입니다.",
            source_summary=source_summary,
        )
        prompt = Prompt(system=system, user=task, context=project)

        # 3. LLM
        result = self.llm_client.complete(prompt)

        # 4. Save under knowledge/<project>/drafts/
        saved_path = knowledge_writer.save(
            category=f"{project}/drafts",
            topic=_topic_slug(task),
            content=result["answer"],
        )

        return {
            "answer":              result["answer"],
            "model":               result["model"],
            "latency_sec":         result["latency_sec"],
            "saved_path":          str(saved_path),
            "strategy_used_count": len(items),
        }
