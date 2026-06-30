"""
Chronos OS — Research Plan

Generated before search. Drives multi-query evidence collection.
"""

from dataclasses import dataclass, field


@dataclass
class ResearchPlan:
    project: str
    task:    str
    queries: list = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"## Research Plan — {self.project}", f"**Task:** {self.task}", "", "**Queries:**"]
        for i, q in enumerate(self.queries, 1):
            lines.append(f"{i}. {q}")
        return "\n".join(lines)
