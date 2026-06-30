"""
Chronos OS — Strategy Pipeline

Athena's flow: read existing project knowledge → build Athena prompt → LLM →
save the strategic interpretation under knowledge/<project>/strategy/.

No web search, no Tavily. Strategy is grounded in already-saved knowledge.
"""

import re
from datetime import datetime

from core.prompt import Prompt
from core.strategy_output import SECTION_TITLES


def _topic_slug(task: str) -> str:
    date = datetime.now().strftime("%Y%m%d")
    slug = re.sub(r"[^\w]", "_", task[:40].strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return f"{date}_{slug}"


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _missing_sections(answer: str) -> list:
    """Return required section titles not found in the answer (heading check only)."""
    norm = _normalize(answer)
    return [t for t in SECTION_TITLES if _normalize(t) not in norm]


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

        # 2. Build Athena prompt grounded in that knowledge (no new research).
        #    Require the exact 7 StrategyOutput sections so results are consistent
        #    and directly usable for STP slide planning.
        section_list = "\n".join(f"{i}. {t}" for i, t in enumerate(SECTION_TITLES, 1))
        context = (
            f"현재 작업은 '{project}' 프로젝트의 전략 해석입니다.\n"
            f"반드시 아래 7개 섹션 제목을 영문 그대로, 마크다운 헤딩으로 사용해 출력하세요:\n"
            f"{section_list}"
        )
        system = athena.build_system_prompt(context=context, source_summary=source_summary)
        prompt = Prompt(system=system, user=task, context=project)

        # 3. LLM
        result = self.llm_client.complete(prompt)

        # 3b. Validate required section headings are present (no complex parsing yet)
        missing = _missing_sections(result["answer"])
        required_present = not missing
        print(f"  [strategy] required sections present: {required_present}"
              + (f"  missing: {missing}" if missing else ""))

        # 4. Save under knowledge/<project>/strategy/
        saved_path = knowledge_writer.save(
            category=f"{project}/strategy",
            topic=_topic_slug(task),
            content=result["answer"],
        )

        return {
            "answer":                   result["answer"],
            "model":                    result["model"],
            "latency_sec":              result["latency_sec"],
            "saved_path":               str(saved_path),
            "knowledge_used_count":     len(items),
            "required_sections_present": required_present,
            "missing_sections":         missing,
        }
