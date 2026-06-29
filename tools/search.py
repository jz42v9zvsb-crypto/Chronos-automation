"""
Chronos OS — Search Abstraction

Hermes uses SearchProvider, never a concrete provider directly.
Swap the provider without touching Hermes.
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime


class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> dict:
        """
        Run a search query.

        Returns:
            {
                "query":       str,
                "results":     list[dict],  # each has "url", "title", "content"
                "provider":    str,
                "searched_at": str,         # ISO 8601 UTC
            }
        """


class TavilySearchProvider(SearchProvider):
    PROVIDER_NAME = "tavily"

    def __init__(self, config: dict = None):
        config = config or {}
        api_key = config.get("TAVILY_API_KEY") or os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError(
                "[TavilySearchProvider] TAVILY_API_KEY not found — "
                "add it to .env or set it as an environment variable"
            )
        from tavily import TavilyClient
        self._client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5) -> dict:
        raw = self._client.search(query=query, max_results=max_results)
        results = [
            {
                "url":     r.get("url", ""),
                "title":   r.get("title", ""),
                "content": r.get("content", ""),
                "score":   r.get("score"),
            }
            for r in raw.get("results", [])
        ]
        return {
            "query":       query,
            "results":     results,
            "provider":    self.PROVIDER_NAME,
            "searched_at": datetime.utcnow().isoformat(),
        }
