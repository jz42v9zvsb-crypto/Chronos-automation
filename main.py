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


if __name__ == "__main__":
    main()
