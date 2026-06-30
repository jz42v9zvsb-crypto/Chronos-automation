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

All commits below landed 2026-06-29. Grouped by theme.

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
- `62dde63` add ResearchContext and interactive pipeline  *(current `main` tip)*

---

## Current Sprint — Project-context-driven planned research (in progress)

Present in the working tree, **not yet committed**:

- `core/project_loader.py` — loads `contexts/<project>/` into a ProjectContext
- `core/research_plan.py` — research plan model
- `tools/planner.py` — `SimpleResearchPlanner` (generates planned queries)
- `contexts/` — first project context (`amway-stp/`)
- modifications to `core/boot.py`, `core/research_pipeline.py`, `main.py` to wire
  the planner + project loader into the pipeline

Goal: drive research from a per-project context and a multi-query plan instead of a
single ad-hoc query.

---

## Next Planned Sprints

Sourced from README.md's stated agent plan and existing technical debt — not invented.

- **Additional agents** (README marks these 🔜):
  - Athena — interpretation / strategy
  - Apollo — script / content
  - Hephaestus — automation / code / API
  - Zeus — routing / orchestration (planned last)
- **Provider abstraction** — remove the hardcoded OpenAI dependency in `main.py`
  and the pipeline so providers are truly interchangeable (per `CLAUDE.md §9`).
- **Consolidate Hermes** — resolve the duplicate `agents/hermes.py` vs
  `agents/hermes_v2.py` (only v2 is wired) per `CLAUDE.md §2`.
- **Commit & push the current slice**, then push the 12 local commits to origin.
