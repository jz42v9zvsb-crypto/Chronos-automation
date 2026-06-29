"""
Chronos OS — Prompt

Standard object passed from Chronos to any LLM client.
Decouples prompt construction from model provider.
"""

from dataclasses import dataclass


@dataclass
class Prompt:
    system:  str
    user:    str
    context: str

    def to_openai_messages(self) -> list:
        return [
            {"role": "system", "content": self.system},
            {"role": "user",   "content": self.user},
        ]
