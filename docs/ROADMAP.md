# Chronos OS — Roadmap

> Derived from git history, CHANGELOG.md, README.md, and the current project
> structure. No information here is invented; items that are planned-but-not-built
> are marked as such and sourced from README.md's stated intentions.

---

## Vision

Chronos OS is 류안영's personal AI operating system — not a prompt collection.

- A **team of role-specialized agents** beats one agent that does everything.
- Research **accumulates** and stays connected (knowledge is persisted, not thrown away).
- The **model is an interchangeable engine** — Chronos must never depend on a
  specific provider (Claude / GPT / Gemini / OpenRouter).
- **Working software over cleaner software**; small validated changes over rewrites.

---

## Architecture

On-disk structure (the immutable tree per `CLAUDE.md §8`):

```
core/      boot.py, context.py, evidence.py, prompt.py,
           research_pipeline.py, research_plan.py*, project_loader.py*
agents/    hermes.py, hermes_v2.py
tools/     openai_client.py, search.py, knowledge_writer.py, planner.py*
knowledge/ (research output store — currently empty)
contexts/* per-project context (amway-stp/: audience, constraints, objective, references)
identity/  who_is_ryu.md, goals, principles, decision_framework
standards/ luxury, ppt, research, sources, writing
persona/   5 audience persona files
hermes/    mission, principles, output_format, tools, examples (Hermes constitution)
shared/    routing.md
```
`*` = present in working tree but not yet committed.

**Runtime flow** (`main.py` → `Chronos.research()`):

```
ProjectLoader → Planner → Search (Tavily) → Evidence → Prompt (Hermes) → LLM (OpenAI) → KnowledgeWriter
```

`Chronos` (`core/boot.py`) is the kernel: boots config + identity, validates folder
structure, and owns the agent registry (`register` / `route` / `ask` / `research`).

---

## Completed Sprints

Grouped by theme. Sprints 1–5 landed 2026-06-29; Sprints 6–9 on 2026-06-30.

### Sprint 1 — Foundation & structure
- `ae62c98` Initial commit
- `3cc9574` Hermes v1.0 헌법 초안
- `80c5854` Chronos OS v2.0 구조 재설계
- `a4b966f` Chronos OS v2.1 구조 재설계 — knowledge/contexts/persona/identity/standards 추가
- `bbda169` bootstrap Chronos OS and Hermes v2
- `bcf3adc` add .gitignore and clean repository
- `a0b07c9` add Commit Rules section to CLAUDE.md

### Sprint 2 — LLM integration
- `c90c017` Chronos.ask() — returns API-ready payload via Hermes
- `3d04ebb` add OpenAIClient and wire LLM call in main.py
- `f3dd39f` first LLM client integration

### Sprint 3 — Research pipeline
- `37904cc` add KnowledgeWriter
- `1d80b87` add search provider abstraction and Tavily provider
- `8877305` add ResearchPipeline
- `a0edfe1` add Evidence layer
- `ea8c68c` add Prompt object
- `62dde63` add ResearchContext and interactive pipeline

### Sprint 4 — Project-context-driven planned research
Drive research from a per-project context and a multi-query plan instead of a single
ad-hoc query. `ProjectLoader` reads `contexts/<project>/`, `SimpleResearchPlanner`
generates planned queries, both wired into the pipeline.
- `61e0828` feat(core): add project-aware research planner
  (`core/project_loader.py`, `core/research_plan.py`, `tools/planner.py`, `contexts/`,
  plus pipeline/boot/main wiring)

### Sprint 5 — Knowledge reuse (KnowledgeReader)
Read existing saved knowledge from `knowledge/<project>/` and inject it into the
research prompt before new search evidence, so research accumulates. Deterministic;
no embeddings, no LLM, no vector database.
- `259fc61` feat(knowledge): add KnowledgeReader
  (`tools/knowledge_reader.py`, plus `research_pipeline`/`boot`/`main` threading and
  the `knowledge_used_count` output field)
- `82eb3a9` docs(knowledge): refresh amway-stp research output

### Sprint 6 — Athena 0.1 (strategy agent)
New strategy agent that interprets accumulated Hermes knowledge into strategic
direction. No web search; grounded in saved knowledge. `chronos.strategy()` wired;
saves under `knowledge/<project>/strategy/`.
- `202aa7a` feat(athena): add Athena strategy agent and strategy pipeline
  (`agents/athena_v1.py`, `athena/` constitution, `core/strategy_pipeline.py`,
  nested `KnowledgeWriter` category paths)
- `a6463f9` docs(knowledge): refresh amway-stp research and add Athena strategy output

### Sprint 7 — Evidence quality (Hermes)
Deduplicate, classify source quality, confidence-label, and rank evidence before it
reaches the LLM. Deterministic; no embeddings/LLM/vector DB.
- `77607e5` feat(evidence): add evidence dedup, ranking, and source validation
  (`core/evidence_quality.py`, `Evidence` source_type/confidence fields, pipeline
  raw/processed + High/Med/Low confidence counts)

### Sprint 8 — Structured strategy output (Athena)
Athena emits a fixed 7-section report (Core Insight → Recommended Narrative) for
consistent, deck-ready STP planning; pipeline validates section presence.
- `e9885f0` feat(athena): add structured strategy output
  (`core/strategy_output.py` + `SECTION_TITLES`, required_sections_present /
  missing_sections)

### Sprint 9 — Project-aware strategy (Athena)
Strategy interprets knowledge through the project context (`contexts/<project>/` via
the existing `ProjectLoader`). Prompt keeps PROJECT CONTEXT / EXISTING KNOWLEDGE /
STRATEGIC INTERPRETATION distinct.
- `ea7db5b` feat(athena): add project-aware strategy context
  (project_context_used / project_context_empty metadata)

### Sprint 10 — Strategy handoff format (Athena)
Athena emits a final "Strategy Handoff" section (section 8, 9 sub-sections) so
strategy can pass cleanly to a future writing/deck agent without reinterpretation.
Athena remains strategy-only (Apollo not implemented).
- `3e913ce` feat(athena): add strategy handoff format
  (`core/strategy_handoff.py` + `HANDOFF_SECTION_TITLE`/`HANDOFF_SUBSECTIONS`,
  prompt requirement + presence validation, `handoff_section_present`)

### Sprint 11 — Deterministic strategy quality check (Athena)
Deterministic gate on Athena output before it is considered usable: required
sections, handoff presence, and risky/absolute phrasing → Pass/Review/Fail. No LLM,
no embeddings.
- `d4df3ed` feat(athena): add deterministic strategy quality check
  (`core/strategy_quality.py`, pipeline routes validation through the checker and
  removes duplicate section logic; strategy_quality_label / strategy_missing_sections
  / strategy_risky_phrases / strategy_handoff_present)

---

## Current Sprint

None in progress. Latest completed: Sprint 11 (deterministic strategy quality check).

---

## Next Planned Sprints

Sourced from README.md's stated agent plan and existing technical debt — not invented.

- **Remaining agents** (README marks these 🔜):
  - Apollo — script / content
  - Hephaestus — automation / code / API
  - Zeus — routing / orchestration (planned last)
- **Strategy parsing** — populate `StrategyOutput` / `StrategyHandoff` fields from
  Athena's markdown (deferred — currently heading-presence validation only).
- **Provider abstraction** — remove the hardcoded OpenAI dependency in `main.py`
  and the pipeline so providers are truly interchangeable (per `CLAUDE.md §9`).
- **Consolidate Hermes** — resolve the duplicate `agents/hermes.py` vs
  `agents/hermes_v2.py` (only v2 is wired) per `CLAUDE.md §2`.
