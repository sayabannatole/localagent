from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.agents.architecture import ArchitectureAgent
from app.agents.base import AgentRequest

router = APIRouter()


class ArchInput(BaseModel):
    problem: str               # describe the system / feature to design
    context: str = ""          # team size, tech stack, constraints, NFRs


class AgentResponse(BaseModel):
    result: str


@router.post("/", response_model=AgentResponse)
async def architecture_design(body: ArchInput, request: Request):
    """
    Generate architecture design and an ADR for a given problem.

    - **problem**: describe the system, feature, or decision to design
    - **context**: optional — team constraints, existing stack, NFRs
    """
    agent = ArchitectureAgent(request.app.state.llm)
    result = agent.design(AgentRequest(payload=body.problem, context=body.context))
    return AgentResponse(result=result)
