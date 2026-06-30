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
from core.evidence_quality import EvidenceQualityProcessor


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
            evidence_quality_processor=EvidenceQualityProcessor(),
        )
        print("\n" + "─" * 50)
        print(result["answer"])
        print("─" * 50)
        print(f"  model    : {result['model']}")
        print(f"  latency  : {result['latency_sec']}s")
        print(f"  evidence : {result['evidence_count_processed']}/{result['evidence_count_raw']} (processed/raw)")
        print(f"  conf     : High {result['evidence_high_confidence_count']} / "
              f"Med {result['evidence_medium_confidence_count']} / "
              f"Low {result['evidence_low_confidence_count']}")
        print(f"  knowledge: {result['knowledge_used_count']} prior file(s)")
        print(f"  saved    : {result['saved_path']}")
        if result.get("research_plan"):
            print("\n" + result["research_plan"])
        print("─" * 50)

        # 2. Strategy (Athena) — interpret the saved research, no web search
        strategy = chronos.strategy(
            project="amway-stp",
            task="은준세 STP 자료를 바탕으로 STP 장표의 전략적 메시지 구조를 제안해줘",
        )
        print("\n" + "═" * 50)
        print("  ATHENA — Strategic Interpretation")
        print("═" * 50)
        print(strategy["answer"])
        print("─" * 50)
        print(f"  model    : {strategy['model']}")
        print(f"  latency  : {strategy['latency_sec']}s")
        print(f"  knowledge: {strategy['knowledge_used_count']} prior file(s)")
        print(f"  project  : used={strategy['project_context_used']} empty={strategy['project_context_empty']}")
        print(f"  sections : {'all present' if strategy['required_sections_present'] else 'INCOMPLETE'}")
        if strategy["missing_sections"]:
            print(f"  missing  : {strategy['missing_sections']}")
        print(f"  saved    : {strategy['saved_path']}")
        print("─" * 50)
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
