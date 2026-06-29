"""
Chronos OS — Hermes Agent
==========================
Research Director.
사실만 수집한다. 의견은 내지 않는다.
출처 없는 수치는 쓰지 않는다.
"""

from pathlib import Path


class Hermes:
    NAME = "hermes"
    VERSION = "1.1"

    def __init__(self, root: Path):
        self.root = root
        self.constitution = ""
        self.output_format = {}
        self.ready = False

    def load(self):
        """agents/hermes/ 폴더에서 헌법 파일 로드"""
        hermes_dir = self.root / "agents" / "hermes"

        files = {
            "constitution": hermes_dir / "constitution.md",
            "mission":      hermes_dir / "mission.md",
            "principles":   hermes_dir / "principles.md",
            "output_format": hermes_dir / "output_format.md",
        }

        loaded = []
        combined = []

        for name, path in files.items():
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                combined.append(f"# {name.upper()}\n{content}")
                loaded.append(name)
            else:
                print(f"  [hermes] ⚠️  {name}.md not found — skipping")

        self.constitution = "\n\n---\n\n".join(combined)
        self.ready = len(loaded) > 0

        print(f"  [hermes] loaded: {loaded} ({len(self.constitution)} chars)")
        return self

    def handle(self, task: str, context: str = "gamdo") -> str:
        """
        태스크 수신 → 컨텍스트 확인 → 리서치 준비 메시지 반환

        context: gamdo | amway | axis | investment
        """
        if not self.ready:
            return "[Hermes] ❌ 헌법 파일 로드 실패 — agents/hermes/ 폴더를 확인하세요"

        context_map = {
            "gamdo":      "감도 채널 (luxury brand research)",
            "amway":      "Amway Korea STP",
            "axis":       "AXIS 성형외과",
            "investment": "주식/투자",
        }

        context_label = context_map.get(context, context)

        return (
            f"\n{'─'*50}\n"
            f"  HERMES v{self.VERSION} — Research Director\n"
            f"{'─'*50}\n"
            f"  📋 Task    : {task}\n"
            f"  🗂️  Context : {context_label}\n"
            f"  📚 Constitution: {len(self.constitution)} chars loaded\n"
            f"{'─'*50}\n"
            f"  ⚡ Ready to research. Claude API 연결 시 실행됩니다.\n"
        )

    def build_system_prompt(self, context: str = "gamdo") -> str:
        """Claude API 호출 시 system prompt로 사용할 텍스트 반환"""
        context_instructions = {
            "gamdo": "현재 작업은 감도 유튜브 채널용 luxury brand research입니다. 스크립트에 바로 쓸 수 있는 팩트를 수집하세요.",
            "amway": "현재 작업은 Amway Korea STP 자료조사입니다. PPT 슬라이드에 바로 쓸 수 있는 데이터를 수집하세요.",
            "axis":  "현재 작업은 AXIS 성형외과 관련 리서치입니다.",
            "investment": "현재 작업은 주식/투자 관련 리서치입니다.",
        }

        return f"{self.constitution}\n\n---\n\n{context_instructions.get(context, '')}"
