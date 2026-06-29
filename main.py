"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

import openai
from core.boot import Chronos
from core.context import ResearchContext
from core.research_pipeline import ResearchPipeline
from agents.hermes_v2 import HermesAgent
from tools.search import TavilySearchProvider
from tools.openai_client import OpenAIClient
from tools.knowledge_writer import KnowledgeWriter


def prompt_input(label: str, hint: str = "") -> str:
    if hint:
        print(f"\n{label} ({hint}):")
    else:
        print(f"\n{label}:")
    return input("> ").strip()


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

    project = prompt_input("Project", "gamdo / amway / axis / investment")
    persona = prompt_input("Persona", "luxury_customer / young_mom / second_millennial / millennial / silver")
    output  = prompt_input("Output",  "ppt / youtube / report / notes")
    depth   = prompt_input("Depth",   "snapshot / standard / deep")
    task    = prompt_input("Task")

    ctx = ResearchContext(
        project=project,
        persona=persona,
        output=output,
        depth=depth,
    )

    try:
        result = pipeline.run(task=task, ctx=ctx)
        print("\n" + "─" * 50)
        print(result["answer"])
        print("─" * 50)
        print(f"  model   : {result['model']}")
        print(f"  latency : {result['latency_sec']}s")
        print(f"  saved   : {result['saved_path']}")
        print("─" * 50)
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
