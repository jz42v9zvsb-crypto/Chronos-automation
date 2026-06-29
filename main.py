"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from core.boot import Chronos
from agents.hermes_v2 import HermesAgent
import openai
from tools.openai_client import OpenAIClient


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

    try:
        client = OpenAIClient(chronos.config)
        response = client.complete(payload)
        print("─" * 50)
        print(response)
        print("─" * 50)
    except RuntimeError as e:
        print(f"\n{e}\n")
    except openai.OpenAIError as e:
        print(f"\n[OpenAIClient] API error: {e}\n")


if __name__ == "__main__":
    main()
