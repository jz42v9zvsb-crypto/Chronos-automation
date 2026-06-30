"""
Chronos OS — Strategy Handoff

A clean contract for passing Athena's strategy to a FUTURE writing/deck agent
(Apollo — not implemented yet) without re-interpreting strategy.

This defines the handoff schema only. The strategy pipeline asks Athena to emit a
matching "Strategy Handoff" section and validates its presence (no parsing yet).
"""

from dataclasses import dataclass


HANDOFF_SECTION_TITLE = "Strategy Handoff"

# Required sub-sections inside the Strategy Handoff section (single source of truth
# for the prompt requirement and the output_format contract).
HANDOFF_SUBSECTIONS = [
    "Strategic Thesis",
    "Target Audience",
    "Audience Problem",
    "Desired Shift",
    "Key Messages",
    "Proof Points",
    "Suggested Slide Sequence",
    "Caution Notes",
    "Next Agent Instruction",
]


@dataclass
class StrategyHandoff:
    project: str
    task: str
    source_knowledge_paths: list[str]
    strategic_thesis: str
    target_audience: str
    audience_problem: str
    desired_shift: str
    key_messages: list[str]
    proof_points: list[str]
    slide_sequence: list[str]
    caution_notes: list[str]
    next_agent_instruction: str

    def to_markdown(self) -> str:
        def _bullets(items: list) -> str:
            return "\n".join(f"- {x}" for x in items) if items else "- (none)"

        def _numbered(items: list) -> str:
            return "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1)) if items else "1. (none)"

        return "\n".join([
            f"## {HANDOFF_SECTION_TITLE}",
            f"프로젝트: {self.project}",
            f"과제: {self.task}",
            "",
            "### Source Knowledge",
            _bullets(self.source_knowledge_paths),
            "",
            "### Strategic Thesis",
            self.strategic_thesis,
            "",
            "### Target Audience",
            self.target_audience,
            "",
            "### Audience Problem",
            self.audience_problem,
            "",
            "### Desired Shift",
            self.desired_shift,
            "",
            "### Key Messages",
            _bullets(self.key_messages),
            "",
            "### Proof Points",
            _bullets(self.proof_points),
            "",
            "### Suggested Slide Sequence",
            _numbered(self.slide_sequence),
            "",
            "### Caution Notes",
            _bullets(self.caution_notes),
            "",
            "### Next Agent Instruction",
            self.next_agent_instruction,
        ])
