from app.agents.base import BaseAgent, AgentRequest

CODE_REVIEW_INSTRUCTION = """
Perform a thorough senior-level code review. Your output MUST include these sections:

## Summary
One-paragraph overview of what the code does and overall quality.

## Critical Issues  🔴
Bugs, security vulnerabilities, data-loss risks. Must be fixed before merge.

## Major Concerns  🟠
Performance bottlenecks, design smells, scalability problems. Should be fixed.

## Minor Suggestions  🟡
Style, naming, small improvements. Nice to have.

## Positive Observations  ✅
What's done well — always include this.

## Refactored Snippet (if applicable)
Provide a concrete improved version of the most problematic section.

Be specific: reference line numbers or function names from the submitted code.
""".strip()


class CodeReviewAgent(BaseAgent):
    def review(self, req: AgentRequest) -> str:
        return self.run(req, CODE_REVIEW_INSTRUCTION)
