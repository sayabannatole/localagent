from app.agents.base import BaseAgent, AgentRequest

PR_SUMMARY_INSTRUCTION = """
Summarise this pull request diff as a senior developer writing for reviewers.

## What Changed
Concise bullet list of all meaningful changes grouped by concern
(e.g. business logic, infrastructure, tests, config).

## Why It Changed (Inferred)
Your best inference of the intent/motivation behind the change.

## Risk Assessment
- **Breaking changes**: Yes / No — explain if Yes
- **Test coverage**: Adequate / Insufficient / Unknown
- **Deployment considerations**: migrations, feature flags, rollback plan

## Review Checklist
Generate a targeted checklist that reviewers should verify for THIS specific PR.

## One-Line PR Description
A single sentence suitable for a changelog or release note.
""".strip()


class PRSummaryAgent(BaseAgent):
    def summarise(self, req: AgentRequest) -> str:
        return self.run(req, PR_SUMMARY_INSTRUCTION)
