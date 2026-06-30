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
from core.strategy_handoff import HANDOFF_SECTION_TITLE, HANDOFF_SUBSECTIONS
from core.strategy_quality import StrategyQualityChecker


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

    def run(self, project: str, task: str, athena, knowledge_writer, project_ctx=None) -> dict:
        # 1. Read existing project knowledge (Hermes research)
        items          = self.knowledge_reader.read_project_knowledge(project)
        source_summary = self.knowledge_reader.to_markdown(items)
        print(f"  [strategy] {len(items)} knowledge file(s) loaded")

        # 1b. Project context (contexts/<project>/) — the lens for interpretation
        project_context_md    = project_ctx.to_markdown() if project_ctx is not None else ""
        project_context_empty = project_ctx is None or project_ctx.is_empty()
        project_context_used  = bool(project_context_md)
        print(f"  [strategy] project context: used={project_context_used} empty={project_context_empty}")

        # 2. Build Athena prompt: PROJECT CONTEXT → EXISTING KNOWLEDGE → STRATEGIC
        #    INTERPRETATION. Require the exact 7 StrategyOutput sections so results
        #    are consistent and directly usable for STP slide planning.
        section_list = "\n".join(f"{i}. {t}" for i, t in enumerate(SECTION_TITLES, 1))
        handoff_subs = "\n".join(f"   - {s}" for s in HANDOFF_SUBSECTIONS)
        context = (
            "# STRATEGIC INTERPRETATION (당신의 과제)\n"
            f"현재 작업은 '{project}' 프로젝트의 전략 해석입니다.\n"
            "위 PROJECT CONTEXT(목표·오디언스·제약)를 렌즈로 삼아 EXISTING KNOWLEDGE를 해석하세요.\n"
            "반드시 아래 섹션 제목을 영문 그대로, 마크다운 헤딩으로 사용해 출력하세요:\n"
            f"{section_list}\n"
            f"{len(SECTION_TITLES) + 1}. {HANDOFF_SECTION_TITLE}\n"
            f"   '{HANDOFF_SECTION_TITLE}' 섹션에는 아래 하위 항목을 모두 포함하세요 "
            "(미래의 글쓰기/덱 에이전트가 전략을 재해석하지 않고 바로 쓸 수 있도록):\n"
            f"{handoff_subs}"
        )
        system = athena.build_system_prompt(
            context=context,
            source_summary=source_summary,
            project_context=project_context_md,
        )
        prompt = Prompt(system=system, user=task, context=project)

        # 3. LLM
        result = self.llm_client.complete(prompt)

        # 3b. Deterministic quality check (sections, handoff, risky phrases).
        #     Single source of validation — no duplicate section logic here.
        quality          = StrategyQualityChecker().check(result["answer"])
        strategy_missing = quality["missing_sections"]      # 8 sections incl. handoff
        risky_phrases    = quality["risky_phrases"]
        handoff_present  = quality["handoff_present"]
        quality_label    = quality["label"]

        # 7-section view (handoff tracked separately) for the required-sections field
        missing          = [s for s in strategy_missing if s != HANDOFF_SECTION_TITLE]
        required_present = not missing
        print(f"  [strategy] quality={quality_label}  sections_ok={required_present}  handoff={handoff_present}")
        if strategy_missing:
            print(f"  [strategy] missing: {strategy_missing}")
        if risky_phrases:
            print(f"  [strategy] risky phrases: {risky_phrases}")

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
            "project_context_used":     project_context_used,
            "project_context_empty":    project_context_empty,
            "handoff_section_present":  handoff_present,
            "strategy_quality_label":   quality_label,
            "strategy_missing_sections": strategy_missing,
            "strategy_risky_phrases":   risky_phrases,
            "strategy_handoff_present": handoff_present,
        }
