"""
Chronos OS — Hermes Agent v2
"""

from pathlib import Path


class HermesAgent:
    NAME = "hermes"
    VERSION = "1.1"

    def __init__(self, root: Path):
        self.root = root
        self.prompt_parts = {}
        self.ready = False

    def load(self):
        hermes_dir = self.root / "hermes"
        files = {
            "mission":       hermes_dir / "mission.md",
            "principles":    hermes_dir / "principles.md",
            "output_format": hermes_dir / "output_format.md",
            "tools":         hermes_dir / "tools.md",
            "examples":      hermes_dir / "examples.md",
        }
        loaded = []
        for name, path in files.items():
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    self.prompt_parts[name] = f.read()
                loaded.append(name)
            else:
                print(f"  [hermes] WARNING: {name}.md not found")

        self.ready = len(loaded) > 0
        total_chars = sum(len(v) for v in self.prompt_parts.values())
        print(f"  [hermes] loaded: {loaded} ({total_chars} chars)")
        return self

    def handle(self, task: str, context: str = "gamdo") -> str:
        if not self.ready:
            return "[Hermes] 프롬프트 파일 로드 실패 — hermes/ 폴더를 확인하세요"

        context_map = {
            "gamdo":      "감도 채널 (luxury brand research)",
            "amway":      "Amway Korea STP",
            "axis":       "AXIS 성형외과",
            "investment": "주식/투자",
        }
        context_label = context_map.get(context, context)
        total_chars = sum(len(v) for v in self.prompt_parts.values())

        lines = [
            "-" * 50,
            "  HERMES v" + self.VERSION + " — Research Director",
            "-" * 50,
            "  Task    : " + task,
            "  Context : " + context_label,
            "  Parts   : " + str(list(self.prompt_parts.keys())) + " (" + str(total_chars) + " chars)",
            "-" * 50,
            "  Ready to research. Claude API 연결 시 실행됩니다.",
        ]
        return "\n" + "\n".join(lines) + "\n"

    def build_system_prompt(self, context: str = "gamdo", search_summary: str = "") -> str:
        context_instructions = {
            "gamdo":      "현재 작업은 감도 유튜브 채널용 luxury brand research입니다.",
            "amway":      "현재 작업은 Amway Korea STP 자료조사입니다.",
            "axis":       "현재 작업은 AXIS 성형외과 관련 리서치입니다.",
            "investment": "현재 작업은 주식/투자 관련 리서치입니다.",
        }

        sections = []
        for k, v in self.prompt_parts.items():
            sections.append("# " + k.upper() + "\n" + v)
            if k == "principles" and search_summary:
                sections.append("# SEARCH RESULTS\n" + search_summary)

        instruction = context_instructions.get(context, "")
        return "\n\n---\n\n".join(sections) + "\n\n---\n\n" + instruction


Hermes = HermesAgent
