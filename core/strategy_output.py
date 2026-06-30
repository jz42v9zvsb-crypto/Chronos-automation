"""
Chronos OS — Strategy Output

Structured contract for Athena strategy results so they are consistent and
directly usable for STP slide planning.

SECTION_TITLES is the single source of truth for the required section headings;
the strategy pipeline validates Athena's output against it.
"""

from dataclasses import dataclass


SECTION_TITLES = [
    "Core Insight",
    "Strategic Angle",
    "Audience Tension",
    "Message Hierarchy",
    "Slide Implications",
    "Weak Claims / Risks",
    "Recommended Narrative",
]


@dataclass
class StrategyOutput:
    project: str
    task: str
    core_insight: str
    strategic_angle: str
    audience_tension: str
    message_hierarchy: list[str]
    slide_implications: list[str]
    weak_claims_or_risks: list[str]
    recommended_narrative: str

    def to_markdown(self) -> str:
        def _numbered(items: list) -> str:
            return "\n".join(f"{i}. {x}" for i, x in enumerate(items, 1)) if items else "1. (none)"

        def _bullets(items: list) -> str:
            return "\n".join(f"- {x}" for x in items) if items else "- (none)"

        return "\n".join([
            "## ATHENA — Strategy Output",
            f"프로젝트: {self.project}",
            f"과제: {self.task}",
            "",
            "## Core Insight",
            self.core_insight,
            "",
            "## Strategic Angle",
            self.strategic_angle,
            "",
            "## Audience Tension",
            self.audience_tension,
            "",
            "## Message Hierarchy",
            _numbered(self.message_hierarchy),
            "",
            "## Slide Implications",
            _bullets(self.slide_implications),
            "",
            "## Weak Claims / Risks",
            _bullets(self.weak_claims_or_risks),
            "",
            "## Recommended Narrative",
            self.recommended_narrative,
        ])
