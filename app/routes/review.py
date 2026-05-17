from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.agents.code_review import CodeReviewAgent
from app.agents.base import AgentRequest

router = APIRouter()


class ReviewInput(BaseModel):
    code: str
    context: str = ""          # language, framework, repo info, etc.


class AgentResponse(BaseModel):
    result: str


@router.post("/", response_model=AgentResponse)
async def code_review(body: ReviewInput, request: Request):
    """
    Submit code for a senior-level review.

    - **code**: raw source code to review
    - **context**: optional — language, framework, PR title, related ticket
    """
    agent = CodeReviewAgent(request.app.state.llm)
    result = agent.review(AgentRequest(payload=body.code, context=body.context))
    return AgentResponse(result=result)
