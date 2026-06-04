# Agent System Design Mock

## Scenario

You are interviewing for an agent-focused AI role. The prompt: "Design an agent that triages incoming
IT support tickets and resolves the easy ones automatically. It can read the ticket, search the
knowledge base, reset passwords, create accounts, and open tickets with other teams. Anything it
cannot resolve should go to a human."

## Round Format

A 60-minute round: 5 minutes clarifying autonomy and risk, 15 minutes on the agent loop and tools, 20
minutes on guardrails and human handoff, 10 minutes on evaluation, and 10 minutes on failure modes.

## Interviewer Prompt

This is an agent design with real, partly irreversible actions. Cover the loop, the tools and their
permissions, how you stop runaway behavior, when a human must approve, and how you evaluate an agent
rather than a single answer.

## Expected Clarification Questions

- Which actions are reversible (search) and which are not (create account, reset password)?
- What is the cost of a wrong automated action versus escalating to a human?
- Is there a budget per ticket (steps, time, tool calls, money)?
- Do we have historical tickets with resolutions to evaluate against?
- What fraction of tickets is the agent expected to resolve versus route?

## Expected Answer or Design

A strong candidate starts by resisting full autonomy. Map tools by risk: read-only tools (search,
read ticket) run freely; state-changing tools (reset password, create account) require validation and,
for the riskiest, human approval. The agent loop: read the ticket, plan, gather context from the
knowledge base, decide an action, call a validated tool, observe, and repeat until resolved or a stop
condition fires. Stop conditions are explicit: max steps, time and token budget, low confidence, or
any high-risk action, all of which trigger escalation with the full trajectory attached.

Guardrails: every tool call validated against a schema, permissioned by ticket type and user, and
logged for audit. The agent never invents a resolution; if the knowledge base lacks an answer it
routes to a human. Evaluation is trajectory-level, not just final answer: task success rate (resolved
correctly), false-resolution rate (closed wrong), steps and cost per ticket, tool-error rate, and
escalation precision. Roll out by starting with read-only triage and routing, then enabling
reversible actions, then carefully gating irreversible ones behind approval.

## Worked Strong Answer Outline

1. Classify tools by reversibility and risk; gate the irreversible ones.
2. Explicit stop conditions: budget, low confidence, high-risk action.
3. Schema-validated, permissioned, audited tool calls.
4. Evaluate the trajectory and false-resolution rate, not just the answer.
5. Stage rollout: triage, then reversible actions, then approved irreversible ones.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Autonomy | Gates irreversible actions, escalates | Full autonomy from day one |
| Loop and tools | Clear loop, schema-validated permissioned tools | Unbounded free-form tool use |
| Guardrails | Budgets, stop conditions, audit log | No limits, no logging |
| Evaluation | Trajectory metrics, false-resolution rate | Only final answer correctness |
| Rollout | Staged by risk | Turns everything on at once |

## Red Flags

- Allowing irreversible actions with no human approval.
- No step, time, or cost budget, so the agent can loop.
- Tools without schemas, permissions, or audit logs.
- Evaluating only the final message, ignoring wrong closures and cost.
- No escalation path for low-confidence or unknown tickets.

## Follow-Up Questions

- The agent reset the wrong user's password. How do you prevent and detect this?
- It loops between search and plan for 30 steps. What stops it and what do you log?
- How do you measure whether escalations are happening at the right time?

## Self-Review Checklist

- Did I classify tools by risk and gate irreversible actions?
- Did I define explicit stop conditions and budgets?
- Did I make tool calls validated, permissioned, and audited?
- Did I evaluate the trajectory and false-resolution rate?
- Did I propose a staged rollout by risk level?

---
## Navigation

[⬅ Previous](05-rag-system-design-mock.md) | [🏠 Home](../README.md) | [➡ Next](07-statistics-mock.md)
