from app.agents.base import BaseAgent, AgentRequest

ARCHITECTURE_INSTRUCTION = """
You are designing or reviewing a software system. Produce a structured response:

## Problem Understanding
Restate the problem in your own words to confirm understanding.

## Proposed Architecture
Describe the recommended architecture with components, data flows, and boundaries.
Include an ASCII diagram if it aids clarity.

## Key Design Decisions
For each major decision, state: Decision → Rationale → Alternatives considered.

## ADR (Architecture Decision Record)
Generate a formal ADR in this format:
  - **Title**: [Short present-tense imperative]
  - **Status**: Proposed
  - **Context**: Why this decision is needed
  - **Decision**: What was decided
  - **Consequences**: Trade-offs, risks, follow-up actions

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

## Next Steps
Concrete, prioritised actions to move from design to implementation.
""".strip()


class ArchitectureAgent(BaseAgent):
    def design(self, req: AgentRequest) -> str:
        return self.run(req, ARCHITECTURE_INSTRUCTION)
