"""
Chronos OS — Strategy Pipeline

Athena's flow: read existing project knowledge → build Athena prompt → LLM →
save the strategic interpretation under knowledge/<project>/strategy/.

No web search, no Tavily. Strategy is grounded in already-saved knowledge.
"""

import re
from datetime import datetime

from core.prompt import Prompt


def _topic_slug(task: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    slug = re.sub(r"[^\w]", "_", task[:40].strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return f"{date}_{slug}"


class StrategyPipeline:
    def __init__(self, chronos, llm_client, knowledge_reader):
        self.chronos          = chronos
        self.llm_client       = llm_client
        self.knowledge_reader = knowledge_reader

    def run(self, project: str, task: str, athena, knowledge_writer) -> dict:
        # 1. Read existing project knowledge (Hermes research)
        items          = self.knowledge_reader.read_project_knowledge(project)
        source_summary = self.knowledge_reader.to_markdown(items)
        print(f"  [strategy] {len(items)} knowledge file(s) loaded")

        # 2. Build Athena prompt grounded in that knowledge (no new research)
        system = athena.build_system_prompt(
            context=f"현재 작업은 '{project}' 프로젝트의 전략 해석입니다.",
            source_summary=source_summary,
        )
        prompt = Prompt(system=system, user=task, context=project)

        # 3. LLM
        result = self.llm_client.complete(prompt)

        # 4. Save under knowledge/<project>/strategy/
        saved_path = knowledge_writer.save(
            category=f"{project}/strategy",
            topic=_topic_slug(task),
            content=result["answer"],
        )

        return {
            "answer":               result["answer"],
            "model":                result["model"],
            "latency_sec":          result["latency_sec"],
            "saved_path":           str(saved_path),
            "knowledge_used_count": len(items),
        }
