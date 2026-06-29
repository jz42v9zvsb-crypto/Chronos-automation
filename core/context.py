"""
Chronos OS — Research Context

Carries all user intent into the pipeline:
who it's for, what format, how deep.
"""

from dataclasses import dataclass


@dataclass
class ResearchContext:
    project:  str           # gamdo | amway | axis | investment
    persona:  str           # luxury_customer | young_mom | second_millennial | millennial | silver
    output:   str           # ppt | youtube | report | notes
    depth:    str           # snapshot | standard | deep
    language: str = "ko"
