"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

import openai
from core.boot import Chronos
from agents.hermes_v2 import HermesAgent
from tools.planner import SimpleResearchPlanner
from tools.knowledge_reader import KnowledgeReader


def main():
    chronos = Chronos()
    chronos.boot()

    hermes = HermesAgent(chronos.root)
    hermes.load()
    chronos.register("hermes", hermes)

    try:
        result = chronos.research(
            project="amway-stp",
            task="은준세 STP를 보강할 백그라운드 자료를 조사해줘",
            planner=SimpleResearchPlanner(),
            knowledge_reader=KnowledgeReader(chronos.root),
        )
        print("\n" + "─" * 50)
        print(result["answer"])
        print("─" * 50)
        print(f"  model    : {result['model']}")
        print(f"  latency  : {result['latency_sec']}s")
        print(f"  evidence : {result['evidence_count']} results")
        print(f"  knowledge: {result['knowledge_used_count']} prior file(s)")
        print(f"  saved    : {result['saved_path']}")
        if result.get("research_plan"):
            print("\n" + result["research_plan"])
        print("─" * 50)
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
