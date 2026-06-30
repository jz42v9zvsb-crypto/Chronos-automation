"""
Chronos OS — Athena Agent v1

Strategy agent. Interprets Hermes research/knowledge into strategic direction.
Athena does NOT search the web and does NOT collect new facts — it reads
already-saved knowledge and produces grounded interpretation.
"""

from pathlib import Path


class AthenaAgent:
    NAME = "athena"
    VERSION = "0.1"

    def __init__(self, root: Path):
        self.root = root
        self.prompt_parts = {}
        self.ready = False

    def load(self):
        athena_dir = self.root / "athena"
        files = {
            "mission":       athena_dir / "mission.md",
            "principles":    athena_dir / "principles.md",
            "output_format": athena_dir / "output_format.md",
            "examples":      athena_dir / "examples.md",
        }
        loaded = []
        for name, path in files.items():
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    self.prompt_parts[name] = f.read()
                loaded.append(name)
            else:
                print(f"  [athena] WARNING: {name}.md not found")

        self.ready = len(loaded) > 0
        total_chars = sum(len(v) for v in self.prompt_parts.values())
        print(f"  [athena] loaded: {loaded} ({total_chars} chars)")
        return self

    def build_system_prompt(self, context: str = "", source_summary: str = "") -> str:
        """
        Assemble Athena's strategy system prompt.

        source_summary is the existing knowledge (Hermes research) Athena must
        ground its interpretation in. It is injected right after the principles
        so the grounding rules apply to it directly.
        """
        sections = []
        for k, v in self.prompt_parts.items():
            sections.append("# " + k.upper() + "\n" + v)
            if k == "principles" and source_summary:
                sections.append("# SOURCE KNOWLEDGE (Hermes 리서치 결과)\n" + source_summary)

        result = "\n\n---\n\n".join(sections)

        instruction = context.strip()
        if instruction:
            result += "\n\n---\n\n" + instruction
        return result


Athena = AthenaAgent
