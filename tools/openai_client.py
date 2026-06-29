"""
Chronos OS — OpenAI Client
"""

import os
import openai


class OpenAIClient:
    def __init__(self, config: dict, model: str = "gpt-4o-mini"):
        self.model = config.get("OPENAI_MODEL") or os.environ.get("OPENAI_MODEL") or model
        api_key = config.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "[OpenAIClient] OPENAI_API_KEY not found — "
                "add it to .env or set it as an environment variable"
            )
        self._client = openai.OpenAI(api_key=api_key)

    def complete(self, payload: dict) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": payload["system"]},
                {"role": "user",   "content": payload["user"]},
            ],
        )
        return response.choices[0].message.content
