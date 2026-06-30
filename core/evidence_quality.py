"""
Chronos OS — Evidence Quality

Improves raw search evidence before it reaches the LLM:
deduplicate → classify source → label confidence → rank.

Deterministic and simple. No embeddings, no LLM, no vector database.
Operates on the existing core.evidence.Evidence dataclass.
"""

from urllib.parse import urlparse
from datetime import datetime


class EvidenceQualityProcessor:
    # Official / government / institutional sources (highest trust)
    OFFICIAL = (
        "go.kr", "kosis.kr", "nps.or.kr",
        "oecd.org", "worldbank.org", "imf.org", "who.int", "un.org",
    )

    # Research / academic sources
    RESEARCH = (
        "doi.org", "springer.com", "sciencedirect.com",
        "tandfonline.com", "ncbi.nlm.nih.gov", "jstor.org",
    )

    # Low-authority hosts (blogs, forums, content farms)
    WEAK = (
        "blog", "tistory", "blogspot", "wordpress", "medium.com",
        "brunch", "namu.wiki", "reddit", "quora", "forum", "cafe.", "fandom",
    )

    _TIER_RANK = {"official": 0, "research": 1, "press": 2, "weak": 3}
    _CONF_RANK = {"High": 0, "Medium": 1, "Low": 2}

    _USEFUL_SNIPPET_MIN = 20  # chars

    def __init__(self):
        pass

    # ---- public API ----------------------------------------------------

    def process(self, evidence: list) -> list:
        """Deduplicate, label (source_type + confidence), then rank."""
        deduped = self.deduplicate(evidence)
        for item in deduped:
            item.source_type = self.classify_source(item.url)
            item.confidence = self.confidence_label(item)
        return self.rank(deduped)

    def deduplicate(self, evidence: list) -> list:
        """Drop items sharing a URL or a title with an earlier item (first wins)."""
        seen_urls = set()
        seen_titles = set()
        out = []
        for item in evidence:
            url = (item.url or "").strip().lower()
            title = (item.title or "").strip().lower()
            if url and url in seen_urls:
                continue
            if title and title in seen_titles:
                continue
            if url:
                seen_urls.add(url)
            if title:
                seen_titles.add(title)
            out.append(item)
        return out

    def rank(self, evidence: list) -> list:
        """Best first: source tier, then confidence, relevance score, recency."""
        return sorted(evidence, key=self._sort_key)

    def classify_source(self, url: str) -> str:
        """Return one of: official | research | press | weak."""
        host = self._host(url)
        if not host:
            return "weak"  # missing URL is penalized
        if any(host == d or host.endswith("." + d) for d in self.OFFICIAL):
            return "official"
        if "scholar" in host or any(host == d or host.endswith("." + d) for d in self.RESEARCH):
            return "research"
        if any(part in host for part in self.WEAK):
            return "weak"
        return "press"

    def confidence_label(self, evidence_item) -> str:
        """High / Medium / Low based on source type and snippet usefulness."""
        url = (evidence_item.url or "").strip()
        snippet = (evidence_item.snippet or "").strip()
        if not url or not snippet:
            return "Low"

        source_type = evidence_item.source_type or self.classify_source(url)
        useful = len(snippet) >= self._USEFUL_SNIPPET_MIN

        if source_type in ("official", "research") and useful:
            return "High"
        if source_type == "press" and useful:
            return "Medium"
        return "Low"

    # ---- internals -----------------------------------------------------

    def _sort_key(self, item):
        tier = self._TIER_RANK.get(item.source_type, self._TIER_RANK["press"])
        conf = self._CONF_RANK.get(item.confidence, self._CONF_RANK["Low"])
        score = item.score if isinstance(item.score, (int, float)) else 0.0
        recency = self._recency_epoch(item.searched_at)
        # ascending sort → smaller is better; negate score/recency so higher wins.
        # title/url are final deterministic tie-breakers.
        return (tier, conf, -score, -recency, item.title or "", item.url or "")

    @staticmethod
    def _host(url: str) -> str:
        if not url:
            return ""
        try:
            netloc = urlparse(url if "//" in url else "//" + url).netloc.lower()
        except (ValueError, TypeError):
            return ""
        return netloc.split("@")[-1].split(":")[0]

    @staticmethod
    def _recency_epoch(searched_at: str) -> float:
        if not searched_at:
            return 0.0
        try:
            return datetime.fromisoformat(searched_at).timestamp()
        except (ValueError, TypeError):
            return 0.0
