"""
Chronos OS — Research Pipeline

Owns the full research flow:
Search → Evidence → Prompt → LLM → Knowledge
"""

from pathlib import Path


def _format_search_summary(search_data: dict) -> str:
    lines = []
    for i, r in enumerate(search_data["results"], 1):
        lines.append(f"{i}. {r['title']}")
        lines.append(f"   {r['url']}")
        lines.append(f"   {r['content'][:200].strip()}")
        lines.append("")
    lines.append(f"(searched_at: {search_data['searched_at']})")
    return "\n".join(lines)


class ResearchPipeline:
    def __init__(self, chronos, search_provider, llm_client, knowledge_writer):
        self.chronos          = chronos
        self.search_provider  = search_provider
        self.llm_client       = llm_client
        self.knowledge_writer = knowledge_writer

    def run(self, task: str, context: str, category: str, topic: str) -> dict:
        # 1. Search
        search_data    = self.search_provider.search(task)
        search_summary = _format_search_summary(search_data)

        # 2. Prompt
        payload = self.chronos.ask(
            task=task,
            context=context,
            search_summary=search_summary,
        )

        # 3. LLM
        result = self.llm_client.complete(payload)

        # 4. Save
        saved_path = self.knowledge_writer.save(
            category=category,
            topic=topic,
            content=result["answer"],
        )

        return {
            "task":        task,
            "context":     context,
            "search":      search_data,
            "answer":      result["answer"],
            "provider":    result["provider"],
            "model":       result["model"],
            "latency_sec": result["latency_sec"],
            "saved_path":  str(saved_path),
        }
