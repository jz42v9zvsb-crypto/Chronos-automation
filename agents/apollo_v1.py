"""
Chronos OS — Apollo Agent v1

Writing / deck narrative agent. Turns Athena strategy + handoff into slide
narrative and copy. Apollo does NOT search the web, does NOT collect facts, and
does NOT generate PPTX — it drafts writing from the provided strategy.
"""

from pathlib import Path


class ApolloAgent:
    NAME = "apollo"
    VERSION = "0.1"

    def __init__(self, root: Path):
        self.root = root
        self.prompt_parts = {}
        self.ready = False

    def load(self):
        apollo_dir = self.root / "apollo"
        files = {
            "mission":       apollo_dir / "mission.md",
            "principles":    apollo_dir / "principles.md",
            "output_format": apollo_dir / "output_format.md",
            "examples":      apollo_dir / "examples.md",
        }
        loaded = []
        for name, path in files.items():
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    self.prompt_parts[name] = f.read()
                loaded.append(name)
            else:
                print(f"  [apollo] WARNING: {name}.md not found")

        self.ready = len(loaded) > 0
        total_chars = sum(len(v) for v in self.prompt_parts.values())
        print(f"  [apollo] loaded: {loaded} ({total_chars} chars)")
        return self

    def build_system_prompt(self, context: str = "", source_summary: str = "") -> str:
        """
        Assemble Apollo's writing system prompt.

        source_summary is the Athena strategy/handoff Apollo must write from. It
        is injected right after the principles so the grounding rules (no new
        facts, do not silently change strategy) apply to it directly.
        """
        sections = []
        for k, v in self.prompt_parts.items():
            sections.append("# " + k.upper() + "\n" + v)
            if k == "principles" and source_summary:
                sections.append("# STRATEGY SOURCE (Athena 전략/핸드오프)\n" + source_summary)

        result = "\n\n---\n\n".join(sections)

        instruction = context.strip()
        if instruction:
            result += "\n\n---\n\n" + instruction
        return result


Apollo = ApolloAgent
