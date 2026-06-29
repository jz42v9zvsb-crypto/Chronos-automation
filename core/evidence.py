"""
Chronos OS — Evidence

Standard data structure for search results.
Decouples Hermes and ResearchPipeline from any specific search provider.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Evidence:
    provider:    str
    title:       str
    url:         str
    snippet:     str
    score:       Optional[float] = None
    searched_at: str             = ""

    def to_markdown(self, index: int) -> str:
        lines = [
            f"{index}. {self.title}",
            f"   {self.url}",
            f"   {self.snippet}",
        ]
        return "\n".join(lines)


def evidence_list_to_markdown(evidence: list) -> str:
    if not evidence:
        return ""
    parts = [e.to_markdown(i) for i, e in enumerate(evidence, 1)]
    searched_at = evidence[0].searched_at
    return "\n\n".join(parts) + f"\n\n(searched_at: {searched_at})"
