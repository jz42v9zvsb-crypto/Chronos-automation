"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from core.boot import Chronos
from agents.hermes_v2 import HermesAgent
import openai
from tools.openai_client import OpenAIClient
from tools.knowledge_writer import KnowledgeWriter


def main():
    chronos = Chronos()
    chronos.boot()

    hermes = HermesAgent(chronos.root)
    hermes.load()
    chronos.register("hermes", hermes)

    chronos.status()

    payload = chronos.ask(
        task="버버리 Daniel Lee 조사",
        context="gamdo",
    )

    writer = KnowledgeWriter(chronos.root)

    try:
        client = OpenAIClient(chronos.config)
        result = client.complete(payload)
        print("─" * 50)
        print(result["answer"])
        print("─" * 50)
        print(f"  provider : {result['provider']}")
        print(f"  model    : {result['model']}")
        print(f"  latency  : {result['latency_sec']}s")
        if result["usage"]:
            print(f"  tokens   : {result['usage']['total_tokens']}")
        print("─" * 50)

        saved = writer.save(
            category="luxury",
            topic="burberry_daniel_lee",
            content=result["answer"],
        )
        print(f"\nKnowledge saved:\n  {saved.relative_to(chronos.root)}\n")
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
