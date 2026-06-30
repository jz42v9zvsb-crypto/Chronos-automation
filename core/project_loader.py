"""
Chronos OS — Project Loader

Reads contexts/<project>/ files into a ProjectContext.
Lets ResearchPipeline inject project knowledge without manual args.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProjectContext:
    project:     str
    objective:   str = ""
    audience:    str = ""
    constraints: str = ""
    references:  str = ""

    def to_markdown(self) -> str:
        sections = []
        if self.objective:
            sections.append("## 프로젝트 목표\n" + self.objective)
        if self.audience:
            sections.append("## 타겟 오디언스\n" + self.audience)
        if self.constraints:
            sections.append("## 제약 조건\n" + self.constraints)
        if self.references:
            sections.append("## 참고 자료\n" + self.references)
        return "\n\n".join(sections)

    def is_empty(self) -> bool:
        return not any([self.objective, self.audience, self.constraints, self.references])


class ProjectLoader:
    def __init__(self, root: Path):
        self.root = root

    def load(self, project_name: str) -> ProjectContext:
        ctx_dir = self.root / "contexts" / project_name

        def read(filename: str) -> str:
            path = ctx_dir / filename
            return path.read_text(encoding="utf-8").strip() if path.exists() else ""

        ctx = ProjectContext(
            project=project_name,
            objective=read("objective.md"),
            audience=read("audience.md"),
            constraints=read("constraints.md"),
            references=read("references.md"),
        )

        if ctx.is_empty():
            print(f"  [project] WARNING: contexts/{project_name}/ is empty")
        else:
            loaded = [k for k in ["objective", "audience", "constraints", "references"]
                      if getattr(ctx, k)]
            print(f"  [project] {project_name} loaded: {loaded}")

        return ctx
