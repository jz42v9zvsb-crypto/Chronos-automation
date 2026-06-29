"""
Chronos OS — Core Boot
========================
류안영의 AI 운영체제.
특정 서비스에 종속되지 않는다.
모델은 바꿔 끼울 수 있다.
지식은 GitHub에 쌓인다.
"""

import os
from pathlib import Path
from datetime import datetime


VERSION = "0.1.0"
ROOT = Path(__file__).parent.parent


class Chronos:
    VERSION = VERSION

    def __init__(self):
        self.root = ROOT
        self.config = {}
        self.identity = ""
        self.agents = {}
        self.booted_at = None

    def boot(self):
        print(f"\n{'='*50}")
        print(f"  Chronos OS v{self.VERSION}")
        print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        self._load_config()
        self._load_identity()
        self._check_structure()

        self.booted_at = datetime.now()
        print(f"\n✅ Chronos OS v{self.VERSION} boot complete.\n")
        return self

    def _load_config(self):
        """config.yaml 또는 .env에서 설정 로드 + os.environ 병합"""
        env_path = self.root / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        self.config[key.strip()] = val.strip()
            print(f"  [config] .env loaded")
        else:
            print(f"  [config] .env not found — using environment variables only")

        # os.environ으로 덮어쓰기 (환경변수 우선)
        for key, val in os.environ.items():
            self.config[key] = val
        print(f"  [config] os.environ merged ({len(os.environ)} vars)")

    def _load_identity(self):
        """identity/who_is_ryu.md 로드 → self.identity에 저장"""
        identity_path = self.root / "identity" / "who_is_ryu.md"
        if identity_path.exists():
            with open(identity_path, encoding="utf-8") as f:
                self.identity = f.read()
            print(f"  [identity] who_is_ryu.md loaded ({len(self.identity)} chars)")
        else:
            print(f"  [identity] who_is_ryu.md not found — skipping")

    def _check_structure(self):
        """필수 폴더 구조 확인"""
        required = ["core", "agents", "tools", "knowledge", "identity", "contexts"]
        for folder in required:
            path = self.root / folder
            status = "✅" if path.exists() else "❌"
            print(f"  {status} {folder}/")

    def route(self, task: str, context: str = "gamdo") -> str:
        """
        태스크를 적절한 에이전트로 라우팅

        context: gamdo | amway | axis | investment
        """
        print(f"\n[router] task='{task}' context='{context}'")

        agent = self.agents.get("hermes")
        if agent:
            return agent.handle(task, context)
        return "[Chronos] 라우팅 준비 중 — Hermes 에이전트 연결 필요"

    def ask(self, task: str, context: str = "gamdo") -> dict:
        """
        태스크를 Hermes system prompt로 변환 → API-ready payload 반환

        context: gamdo | amway | axis | investment
        Returns: {"system": str, "user": str, "context": str}
        """
        hermes = self.agents.get("hermes")
        if not hermes:
            raise RuntimeError("[Chronos] Hermes agent not registered")

        system_prompt = hermes.build_system_prompt(context)
        return {
            "system": system_prompt,
            "user": task,
            "context": context,
        }

    def register(self, name: str, agent):
        """에이전트 등록"""
        self.agents[name] = agent
        print(f"  [registry] {name} registered")

    def status(self):
        """현재 상태 출력"""
        print(f"\n{'─'*40}")
        print(f"  Chronos OS v{self.VERSION}")
        print(f"  Booted: {self.booted_at}")
        print(f"  Root: {self.root}")
        print(f"  Agents: {list(self.agents.keys()) or 'none yet'}")
        print(f"{'─'*40}\n")


if __name__ == "__main__":
    chronos = Chronos()
    chronos.boot()
    chronos.status()
