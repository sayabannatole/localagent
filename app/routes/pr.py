from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.agents.pr_summary import PRSummaryAgent
from app.agents.base import AgentRequest

router = APIRouter()


class PRInput(BaseModel):
    diff: str                  # raw git diff or description of changes
    context: str = ""          # PR title, linked ticket, repo context


class AgentResponse(BaseModel):
    result: str


@router.post("/summarise", response_model=AgentResponse)
async def pr_summarise(body: PRInput, request: Request):
    """
    Summarise a pull request diff.

    - **diff**: raw `git diff` output or plain description of changes
    - **context**: optional — PR title, ticket number, team conventions
    """
    agent = PRSummaryAgent(request.app.state.llm)
    result = agent.summarise(AgentRequest(payload=body.diff, context=body.context))
    return AgentResponse(result=result)
