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
```

Agents:
- **Hermes** (`agents/hermes_v2.py`, v1.1) — research/fact collection, 5-file constitution.
- **Athena** (`agents/athena_v1.py`, v0.1) — strategy interpretation, 4-file constitution
  (`athena/`). No web search. Now produces a fixed 7-section structured report and
  interprets through project context.

Folders: core / agents / tools / knowledge / contexts / identity / standards / persona /
hermes / athena / shared.

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

## Current branch
`main`, in sync with `origin/main` (all feature commits, docs, and refreshed knowledge
artifacts pushed). Working tree clean.

## Latest commits (most recent first)
- `ea7db5b` feat(athena): add project-aware strategy context
- `e9885f0` feat(athena): add structured strategy output
- `77607e5` feat(evidence): add evidence dedup, ranking, and source validation
- `202aa7a` feat(athena): add Athena strategy agent and strategy pipeline

## Pending work
- None outstanding — code, docs (ROADMAP/CHANGELOG/this summary), and knowledge
  artifacts are committed and pushed.

## Next planned sprint
Candidates (see ROADMAP): **Strategy parsing** (populate `StrategyOutput` from Athena's
markdown), or **Apollo** (content/script agent). Plus provider abstraction and Hermes
consolidation.

## Standing technical debt (unchanged)
- `identity/who_is_ryu.md` is empty (loads 0 chars).
- Duplicate `agents/hermes.py` vs `agents/hermes_v2.py` (only v2 wired).
- Hardcoded OpenAI provider in `main.py` / pipelines vs. CLAUDE.md §9.
