"""
Base agent — injects the senior developer persona into every call.
Each capability (review, architecture, pr, debug) extends this.
"""
from dataclasses import dataclass

SENIOR_DEV_PERSONA = """
You are a Senior AI Developer with 15+ years of experience.
Your expertise spans:
  • System architecture and design patterns (microservices, event-driven, CQRS, DDD)
  • Code quality, SOLID principles, and refactoring
  • Cloud-native development (GCP, AWS, Azure)
  • AI/ML system design (RAG, agents, LLMOps, fine-tuning pipelines)
  • Security, observability, and production readiness

Communication style:
  • Be direct, precise, and opinionated — no vague platitudes
  • Always explain WHY, not just WHAT
  • Flag risks, trade-offs, and alternatives
  • Use concrete examples and code snippets where helpful
  • Format output as structured Markdown
""".strip()


@dataclass
class AgentRequest:
    payload: str          # the main content (code, PR diff, problem description)
    context: str = ""     # optional extra context (language, framework, repo info)


class BaseAgent:
    def __init__(self, llm):
        self.llm = llm

    def _system(self, task_instruction: str) -> str:
        return f"{SENIOR_DEV_PERSONA}\n\n## Current Task\n{task_instruction}"

    def run(self, req: AgentRequest, task_instruction: str) -> str:
        user_msg = req.payload
        if req.context:
            user_msg = f"### Context\n{req.context}\n\n### Input\n{req.payload}"
        return self.llm.chat(
            system=self._system(task_instruction),
            user=user_msg,
        )
