"""
Chronos OS — Entry Point
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from core.boot import Chronos
from agents.hermes_v2 import HermesAgent


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

    print("─" * 50)
    print(f"  context : {payload['context']}")
    print(f"  user    : {payload['user']}")
    print(f"  system  : {len(payload['system'])} chars")
    print("─" * 50)


if __name__ == "__main__":
    main()
