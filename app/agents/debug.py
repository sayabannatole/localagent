from app.agents.base import BaseAgent, AgentRequest

DEBUG_INSTRUCTION = """
You are performing root cause analysis on a reported bug or system failure.

## Problem Restatement
Clarify the exact failure mode in precise technical terms.

## Hypotheses (ranked by likelihood)
List the most probable root causes. For each:
  - Hypothesis
  - Evidence that supports or contradicts it
  - How to confirm/rule it out

## Root Cause (Best Assessment)
State your most likely root cause with confidence level (High / Medium / Low).

## Fix
Provide the concrete fix — code snippet, config change, or command — with explanation.

## Prevention
How to prevent this class of issue from recurring:
  - Code changes
  - Tests to add
  - Monitoring / alerting to set up

## Blast Radius
What else could be affected by this bug or by the proposed fix?
""".strip()


class DebugAgent(BaseAgent):
    def analyse(self, req: AgentRequest) -> str:
        return self.run(req, DEBUG_INSTRUCTION)
