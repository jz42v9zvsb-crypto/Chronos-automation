"""
Chronos OS — OpenAI Client
"""

import os
import time
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

    def complete(self, payload: dict) -> dict:
        t0 = time.perf_counter()
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": payload["system"]},
                {"role": "user",   "content": payload["user"]},
            ],
        )
        latency = time.perf_counter() - t0

        usage = None
        if response.usage:
            usage = {
                "prompt_tokens":     response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens":      response.usage.total_tokens,
            }

        return {
            "answer":      response.choices[0].message.content,
            "provider":    "openai",
            "model":       response.model,
            "usage":       usage,
            "latency_sec": round(latency, 3),
        }
