"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import openai
from core.boot import Chronos
from core.research_pipeline import ResearchPipeline
from agents.hermes_v2 import HermesAgent
from tools.search import TavilySearchProvider
from tools.openai_client import OpenAIClient
from tools.knowledge_writer import KnowledgeWriter


def main():
    chronos = Chronos()
    chronos.boot()

    hermes = HermesAgent(chronos.root)
    hermes.load()
    chronos.register("hermes", hermes)

    pipeline = ResearchPipeline(
        chronos=chronos,
        search_provider=TavilySearchProvider(chronos.config),
        llm_client=OpenAIClient(chronos.config),
        knowledge_writer=KnowledgeWriter(chronos.root),
    )

    try:
        result = pipeline.run(
            task="버버리 Daniel Lee revenue 2024",
            context="gamdo",
            category="luxury",
            topic="burberry_daniel_lee",
        )
        print("─" * 50)
        print(result["answer"])
        print("─" * 50)
        print(f"  model      : {result['model']}")
        print(f"  latency    : {result['latency_sec']}s")
        print(f"  saved      : {result['saved_path']}")
        print("─" * 50)
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
