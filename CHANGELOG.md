# Changelog

All notable changes to Chronos OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `KnowledgeReader` (`tools/knowledge_reader.py`) — reads existing saved knowledge
  from `knowledge/<project>/` and renders it to markdown; deterministic (most-recent
  by modification time), no embeddings/LLM/vector database
- Research pipeline now reads existing project knowledge before new research and
  injects it into the prompt ahead of new search evidence; output dict gains
  `knowledge_used_count`
- `Chronos.research()` and `ResearchPipeline` thread an optional `knowledge_reader`
  dependency; `main.py` instantiates and passes it
- Project-aware research planning — `ProjectLoader` (`contexts/<project>/`),
  `SimpleResearchPlanner`, and `ResearchPlan` wired into the pipeline

## [0.1.0] - 2026-06-29

### Added
- Chronos boot sequence (`core/boot.py`) — loads config, identity, and validates folder structure
- Hermes v2 runtime (`agents/hermes_v2.py`) — research director agent with 5-file constitution loader
- `main.py` entry point — boots Chronos OS and registers Hermes agent
- `CLAUDE.md` engineering constitution — 12 development rules for this codebase
- `.gitignore` — Python, virtualenv, IDE, and OS artifacts excluded
- Commit convention — prefixed commit messages (feat/fix/refactor/docs/test/chore)
- Validation workflow — `py_compile` + import check required before every commit

[Unreleased]: https://github.com/rikimayong/Chronos-automation/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/rikimayong/Chronos-automation/releases/tag/v0.1.0
