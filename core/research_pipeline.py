"""
Chronos OS — Research Pipeline

Owns the full research flow:
Search → Evidence → Prompt → LLM → Knowledge
"""

import re
from datetime import datetime

from core.evidence import evidence_list_to_markdown


def _topic_slug(task: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    slug = re.sub(r"[^\w]", "_", task[:40].strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return f"{date}_{slug}"


class ResearchPipeline:
    def __init__(self, chronos, search_provider, llm_client, knowledge_writer):
        self.chronos          = chronos
        self.search_provider  = search_provider
        self.llm_client       = llm_client
        self.knowledge_writer = knowledge_writer

    def run(self, task: str, ctx) -> dict:
        # 1. Search → Evidence
        search_data    = self.search_provider.search(task)
        evidence       = self.search_provider.to_evidence(search_data)
        search_summary = evidence_list_to_markdown(evidence)

        # 2. Prompt
        prompt = self.chronos.ask(
            task=task,
            ctx=ctx,
            search_summary=search_summary,
        )

        # 3. LLM
        result = self.llm_client.complete(prompt)

        # 4. Save
        saved_path = self.knowledge_writer.save(
            category=ctx.project,
            topic=_topic_slug(task),
            content=result["answer"],
        )

        return {
            "task":        task,
            "context":     ctx.project,
            "search":      search_data,
            "answer":      result["answer"],
            "provider":    result["provider"],
            "model":       result["model"],
            "latency_sec": result["latency_sec"],
            "saved_path":  str(saved_path),
        }
