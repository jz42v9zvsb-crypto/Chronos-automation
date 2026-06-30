# Session Summary — 2026-06-30

## Current architecture
`Chronos` kernel (`core/boot.py`) boots config + identity, validates the folder
structure, and owns the agent registry. Research runtime:

```
ProjectLoader → Planner → Search (Tavily) → Evidence → Prompt (Hermes) → LLM (OpenAI) → KnowledgeWriter
```

One live agent: **Hermes** (`agents/hermes_v2.py`, `HermesAgent` v1.1), loading a
5-file constitution from `hermes/`. Folders: core / agents / tools / knowledge /
contexts / identity / standards / persona / hermes / shared.

## Current Sprint
Project-context-driven planned research — wiring `ProjectLoader` + `SimpleResearchPlanner`
+ `ResearchPlan` + `contexts/` into the pipeline. **In progress, uncommitted.**

## Current branch
`main`, ahead of `origin/main` by 12 commits (none pushed).

## Last commit
`62dde63` — feat(core): add ResearchContext and interactive pipeline (2026-06-29).

## Pending work
- Modified (tracked): `core/boot.py`, `core/research_pipeline.py`, `main.py`
- Untracked: `contexts/`, `core/project_loader.py`, `core/research_plan.py`, `tools/planner.py`
- Plus today's docs additions: `docs/ROADMAP.md`, `docs/session_summary_2026-06-30.md`
  and the earlier `# Session Start Rules` append to `CLAUDE.md`.

## Next objective
Finalize and commit the project-context + planner slice as one coherent feature,
then push the local commits to origin. Before code changes, follow the Session Start
Rules: read CLAUDE.md → ROADMAP → latest session summary → CHANGELOG and summarize.
