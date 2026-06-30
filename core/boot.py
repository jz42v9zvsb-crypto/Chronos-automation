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

from core.prompt import Prompt
from core.context import ResearchContext


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
            with open(env_path, encoding="utf-8") as f:
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

    def ask(self, task: str, ctx: ResearchContext, search_summary: str = "") -> Prompt:
        """
        태스크를 Hermes system prompt로 변환 → Prompt 반환
        """
        hermes = self.agents.get("hermes")
        if not hermes:
            raise RuntimeError("[Chronos] Hermes agent not registered")

        system_base = hermes.build_system_prompt(ctx.project, search_summary=search_summary)
        context_block = (
            f"## 리서치 컨텍스트\n"
            f"- 프로젝트: {ctx.project}\n"
            f"- 페르소나: {ctx.persona}\n"
            f"- 아웃풋: {ctx.output}\n"
            f"- 조사 깊이: {ctx.depth}\n"
            f"- 언어: {ctx.language}\n"
        )
        return Prompt(
            system=system_base + "\n\n---\n\n" + context_block,
            user=task,
            context=ctx.project,
        )

    def research(self, project: str, task: str, planner=None, knowledge_reader=None) -> dict:
        """
        프로젝트 컨텍스트를 자동 로드하고 리서치 파이프라인을 실행한다.

        contexts/<project>/ 파일에서 ProjectContext를 읽어
        ResearchPipeline에 주입한다.
        """
        from core.project_loader import ProjectLoader
        from core.research_pipeline import ResearchPipeline
        from tools.search import TavilySearchProvider
        from tools.openai_client import OpenAIClient
        from tools.knowledge_writer import KnowledgeWriter
        from tools.knowledge_reader import KnowledgeReader

        project_ctx = ProjectLoader(self.root).load(project)

        ctx = ResearchContext(
            project=project,
            persona=project_ctx.audience.split("\n")[0].strip() if project_ctx.audience else "일반",
            output="report",
            depth="standard",
        )

        pipeline = ResearchPipeline(
            chronos=self,
            search_provider=TavilySearchProvider(self.config),
            llm_client=OpenAIClient(self.config),
            knowledge_writer=KnowledgeWriter(self.root),
            planner=planner,
            knowledge_reader=knowledge_reader or KnowledgeReader(self.root),
        )

        return pipeline.run(task=task, ctx=ctx, project_ctx=project_ctx)

    def strategy(self, project: str, task: str) -> dict:
        """
        축적된 지식(Hermes 리서치)을 Athena로 해석해 전략을 생성한다.

        웹 검색을 하지 않는다. knowledge/<project>/를 읽어
        Athena 프롬프트를 만들고 LLM으로 전략 해석을 산출한다.
        """
        from agents.athena_v1 import AthenaAgent
        from core.strategy_pipeline import StrategyPipeline
        from tools.openai_client import OpenAIClient
        from tools.knowledge_writer import KnowledgeWriter
        from tools.knowledge_reader import KnowledgeReader

        athena = AthenaAgent(self.root)
        athena.load()

        pipeline = StrategyPipeline(
            chronos=self,
            llm_client=OpenAIClient(self.config),
            knowledge_reader=KnowledgeReader(self.root),
        )

        return pipeline.run(
            project=project,
            task=task,
            athena=athena,
            knowledge_writer=KnowledgeWriter(self.root),
        )

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
