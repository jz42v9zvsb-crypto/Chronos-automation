"""
Chronos OS — Strategy Quality

Deterministic quality check for Athena strategy outputs before they are treated
as usable. Pure string checks — no LLM, no embeddings.

Required sections reuse the single sources of truth (StrategyOutput.SECTION_TITLES
plus the Strategy Handoff section) so there is no duplicate list to drift.
"""

import re

from core.strategy_output import SECTION_TITLES
from core.strategy_handoff import HANDOFF_SECTION_TITLE


# Phrases that overstate evidence or use absolute language.
RISKY_PHRASES = [
    "확실히", "반드시", "무조건", "입증한다", "증명한다", "유일한", "완벽한",
    "guarantee", "prove", "always", "never",
]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _is_ascii_word(phrase: str) -> bool:
    return phrase.isascii() and phrase.isalpha()


class StrategyQualityChecker:
    def __init__(self):
        pass

    def required_sections(self) -> list[str]:
        return list(SECTION_TITLES) + [HANDOFF_SECTION_TITLE]

    def missing_sections(self, answer: str) -> list[str]:
        norm = _normalize(answer)
        return [s for s in self.required_sections() if _normalize(s) not in norm]

    def risky_phrases(self, answer: str) -> list[str]:
        """Return risky phrases present. English phrases use word boundaries so
        e.g. 'prove' does not match 'approve'; Korean phrases use substring."""
        found = []
        for phrase in RISKY_PHRASES:
            if _is_ascii_word(phrase):
                if re.search(rf"\b{re.escape(phrase)}\b", answer, re.IGNORECASE):
                    found.append(phrase)
            elif phrase in answer:
                found.append(phrase)
        return found

    def has_handoff(self, answer: str) -> bool:
        return _normalize(HANDOFF_SECTION_TITLE) in _normalize(answer)

    def check(self, answer: str) -> dict:
        result = {
            "missing_sections": self.missing_sections(answer),
            "risky_phrases":    self.risky_phrases(answer),
            "handoff_present":  self.has_handoff(answer),
        }
        result["label"] = self.quality_label(result)
        return result

    def quality_label(self, result: dict) -> str:
        missing = result.get("missing_sections", [])
        risky   = result.get("risky_phrases", [])
        handoff = result.get("handoff_present", False)

        if len(missing) >= 3 or not handoff:
            return "Fail"
        if len(missing) >= 1 or risky:
            return "Review"
        return "Pass"
