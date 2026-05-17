from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.agents.debug import DebugAgent
from app.agents.base import AgentRequest

router = APIRouter()


class DebugInput(BaseModel):
    problem: str               # error message, stack trace, or symptom description
    context: str = ""          # relevant code snippet, logs, environment info


class AgentResponse(BaseModel):
    result: str


@router.post("/", response_model=AgentResponse)
async def debug_analysis(body: DebugInput, request: Request):
    """
    Root cause analysis and fix recommendation for a bug or system failure.

    - **problem**: error message, stack trace, or description of the failure
    - **context**: optional — relevant code, logs, environment, recent changes
    """
    agent = DebugAgent(request.app.state.llm)
    result = agent.analyse(AgentRequest(payload=body.problem, context=body.context))
    return AgentResponse(result=result)
