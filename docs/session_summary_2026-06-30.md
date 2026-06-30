# Session Summary — 2026-06-30

## Current architecture
`Chronos` kernel (`core/boot.py`) boots config + identity, validates the folder
structure, and owns the agent registry. Two runtimes:

```
Research (Hermes):
  ProjectLoader → Planner → Search (Tavily) → Evidence → EvidenceQualityProcessor
                → KnowledgeReader (prior knowledge) → Prompt (Hermes) → LLM (OpenAI) → KnowledgeWriter

Strategy (Athena):
  ProjectLoader (contexts/<project>/) + KnowledgeReader (knowledge/<project>/)
                → Prompt (Athena) → LLM (OpenAI) → KnowledgeWriter (knowledge/<project>/strategy/)

Writing (Apollo):
  strategy reader (knowledge/<project>/strategy/) → Prompt (Apollo) → LLM (OpenAI)
                → KnowledgeWriter (knowledge/<project>/drafts/)
```

Agents:
- **Hermes** (`agents/hermes_v2.py`, v1.1) — research/fact collection, 5-file constitution.
- **Athena** (`agents/athena_v1.py`, v0.1) — strategy interpretation, 4-file constitution
  (`athena/`). No web search. Structured 7-section report, project-aware, with handoff +
  deterministic quality gate.
- **Apollo** (`agents/apollo_v1.py`, v0.1) — writing/deck narrative, 4-file constitution
  (`apollo/`). Writes drafts from Athena strategy/handoff; no web search, no fact
  invention, no PPTX.

Folders: core / agents / tools / knowledge / contexts / identity / standards / persona /
hermes / athena / apollo / shared.

## Completed this session
- **KnowledgeReader** — reads accumulated `knowledge/<project>/` into the research prompt.
- **Athena 0.1** — strategy agent + `core/strategy_pipeline.py` + `chronos.strategy()`;
  saves under `knowledge/<project>/strategy/` (nested `KnowledgeWriter` paths).
- **Evidence quality (Hermes)** — `EvidenceQualityProcessor` dedups, classifies source
  quality, confidence-labels, and ranks evidence before the LLM; `Evidence` gains
  `source_type`/`confidence`; pipeline returns raw/processed + High/Med/Low counts.
- **Structured strategy output (Athena)** — `StrategyOutput` + `SECTION_TITLES`; fixed
  7-section report; `required_sections_present` / `missing_sections`.
- **Project-aware strategy (Athena)** — interprets knowledge through `contexts/<project>/`
  (reuses `ProjectLoader`); `project_context_used` / `project_context_empty`.
- **Strategy handoff (Athena)** — `StrategyHandoff`; Athena emits a "Strategy Handoff"
  section (9 sub-sections) for a future writing/deck agent; `handoff_section_present`.
- **Deterministic strategy quality check (Athena)** — `StrategyQualityChecker` gates
  output (sections, handoff, risky phrasing) → Pass/Review/Fail; no LLM/embeddings.
- **Apollo 0.1 (writing/deck agent)** — `WritingPipeline` + `chronos.write()`; turns
  Athena strategy/handoff into a deck draft under `knowledge/<project>/drafts/`.
  Full chain now runs: research → strategy → write.

## Current branch
`main`, in sync with `origin/main` (all feature commits, docs, and refreshed knowledge
artifacts pushed). Working tree clean.

## Latest commits (most recent first)
- `f5970e6` feat(apollo): add Apollo writing/deck agent
- `d4df3ed` feat(athena): add deterministic strategy quality check
- `ea7db5b` feat(athena): add project-aware strategy context
- `e9885f0` feat(athena): add structured strategy output

## Pending work
- None outstanding — code, docs (ROADMAP/CHANGELOG/this summary), and knowledge
  artifacts are committed and pushed.

## Next planned sprint
Candidates (see ROADMAP): **Strategy parsing** (populate `StrategyOutput`/`StrategyHandoff`
from markdown), **KnowledgeReader nested paths**, or **Hephaestus**. Plus provider
abstraction and Hermes
consolidation.

## Standing technical debt (unchanged)
- `identity/who_is_ryu.md` is empty (loads 0 chars).
- Duplicate `agents/hermes.py` vs `agents/hermes_v2.py` (only v2 wired).
- Hardcoded OpenAI provider in `main.py` / pipelines vs. CLAUDE.md §9.
