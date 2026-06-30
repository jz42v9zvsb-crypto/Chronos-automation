"""
Chronos OS — Research Planner

Rule-based query generator. No LLM required.
Future: LLMResearchPlanner subclass.
"""

from core.research_plan import ResearchPlan

_AMWAY_STP_QUERIES = [
    "한국 은퇴 준비 부족 국민연금 평균 수령액 최근 5년",
    "OECD 한국 노후소득보장 pension income elderly poverty",
    "한국 중장년 퇴직 후 재취업 자영업 소득 통계",
    "한국 50대 60대 노후 준비 부족 조사",
    "국민연금공단 평균 연금 수령액 노후 생활비",
]


def _is_amway_stp(task: str, project_ctx) -> bool:
    if project_ctx.project == "amway-stp":
        return True
    haystack = " ".join([project_ctx.objective, project_ctx.audience, task])
    return "은준세" in haystack or "노후" in haystack or "국민연금" in haystack


class SimpleResearchPlanner:
    def plan(self, task: str, project_ctx) -> ResearchPlan:
        if _is_amway_stp(task, project_ctx):
            queries = _AMWAY_STP_QUERIES
        else:
            queries = [task]

        return ResearchPlan(
            project=project_ctx.project,
            task=task,
            queries=queries,
        )
