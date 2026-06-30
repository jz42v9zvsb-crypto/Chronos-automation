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
    def __init__(self, chronos, search_provider, llm_client, knowledge_writer, planner=None, knowledge_reader=None, evidence_quality_processor=None):
        self.chronos                    = chronos
        self.search_provider            = search_provider
        self.llm_client                 = llm_client
        self.knowledge_writer           = knowledge_writer
        self.planner                    = planner
        self.knowledge_reader           = knowledge_reader
        self.evidence_quality_processor = evidence_quality_processor

    def run(self, task: str, ctx, project_ctx=None) -> dict:
        # 0. Read existing project knowledge (before new research)
        existing_knowledge = []
        knowledge_md       = ""
        if self.knowledge_reader:
            existing_knowledge = self.knowledge_reader.read_project_knowledge(ctx.project)
            knowledge_md       = self.knowledge_reader.to_markdown(existing_knowledge)
            print(f"  [knowledge] {len(existing_knowledge)} existing file(s) loaded")

        # 1. Plan → Search → Evidence
        plan     = None
        evidence = []

        if self.planner and project_ctx:
            plan = self.planner.plan(task, project_ctx)
            print(f"  [planner] {len(plan.queries)} queries planned")
            for query in plan.queries:
                try:
                    sd = self.search_provider.search(query, max_results=3)
                    evidence.extend(self.search_provider.to_evidence(sd))
                    print(f"  [search] '{query[:40]}' → {len(sd['results'])} results")
                except RuntimeError as e:
                    print(f"  [search] skipped: {e}")
        else:
            search_data = self.search_provider.search(task)
            evidence    = self.search_provider.to_evidence(search_data)

        # 1b. Quality pass — dedup, rank, confidence-label before the LLM sees it
        processed = evidence
        if self.evidence_quality_processor:
            processed = self.evidence_quality_processor.process(evidence)
            print(f"  [evidence] {len(evidence)} raw → {len(processed)} processed")

        search_summary = evidence_list_to_markdown(processed)

        # Prepend existing knowledge before the new search evidence
        if knowledge_md:
            search_summary = knowledge_md + "\n\n---\n\n" + search_summary

        # Prepend project context if available
        if project_ctx and not project_ctx.is_empty():
            search_summary = project_ctx.to_markdown() + "\n\n---\n\n" + search_summary

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
            "task":          task,
            "context":       ctx.project,
            "research_plan": plan.to_markdown() if plan else None,
            "evidence_count": len(processed),
            "evidence_count_raw": len(evidence),
            "evidence_count_processed": len(processed),
            "evidence_high_confidence_count":   sum(1 for e in processed if e.confidence == "High"),
            "evidence_medium_confidence_count": sum(1 for e in processed if e.confidence == "Medium"),
            "evidence_low_confidence_count":    sum(1 for e in processed if e.confidence == "Low"),
            "knowledge_used_count": len(existing_knowledge),
            "answer":        result["answer"],
            "provider":      result["provider"],
            "model":         result["model"],
            "latency_sec":   result["latency_sec"],
            "saved_path":    str(saved_path),
        }
