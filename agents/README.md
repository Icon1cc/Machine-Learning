# Agents

## Folder Purpose

Agent loops, tool use, planning, memory, multi-agent design, evaluation, observability, and risk controls.

## Beginner Intuition

An agent is an LLM placed in a loop with tools and memory. Instead of answering once, it observes
state, decides an action, calls a tool, observes the result, and repeats until the goal is met or a
stop condition fires. The power comes from acting in the world; the danger comes from the same thing.

## Why It Matters

Agents unlock multi-step automation, but they fail in ways single calls do not: they loop, pick the
wrong tool, compound errors, and can take irreversible real-world actions. Guardrails, budgets,
permissioned tools, and human approval are not optional. Evaluating a trajectory is harder than
grading one answer.

## Who Should Read This Section

Read this if you build autonomous or tool-using systems, or interview for agent-focused AI roles. It
builds on the LLM, RAG, and tool-use material and connects to production-AI and ethics-safety.

## Recommended Reading Order

Read in order: what an agent is, the agent loop, tools and function calling, planning, memory, single
vs multi-agent, agentic RAG, workflow agents, autonomous risks, evaluation, observability, then system
design and interview patterns.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is An AI Agent](01-what-is-an-ai-agent.md) |
| 2 | [Agent Loop](02-agent-loop.md) |
| 3 | [Tools And Function Calling](03-tools-and-function-calling.md) |
| 4 | [Planning And Reasoning](04-planning-and-reasoning.md) |
| 5 | [Memory In Agents](05-memory-in-agents.md) |
| 6 | [Single Agent Vs Multi Agent](06-single-agent-vs-multi-agent.md) |
| 7 | [Agentic RAG](07-agentic-rag.md) |
| 8 | [Workflow Agents](08-workflow-agents.md) |
| 9 | [Autonomous Agents Risks](09-autonomous-agents-risks.md) |
| 10 | [Agent Evaluation](10-agent-evaluation.md) |
| 11 | [Agent Observability](11-agent-observability.md) |
| 12 | [Agent System Design](12-agent-system-design.md) |
| 13 | [Agent Interview Patterns](13-agent-interview-patterns.md) |

## Real-World Examples

- An IT-support agent that reads tickets, searches a knowledge base, and resets passwords with
  approval.
- A coding agent that plans, edits files, runs tests, and reads failures.
- A research agent that searches, reads, and composes a cited report.
- A workflow agent that fills forms and routes approvals across systems.

## Pattern Recognition

- "One LLM call cannot do it; it needs steps and tools" points to an agent.
- "It loops forever" points to missing stop conditions and budgets.
- "It took an irreversible action wrongly" points to missing human approval gates.
- "It works in demos but not at scale" points to missing trajectory evaluation and observability.

## Common Mistakes

- Building a multi-agent system when one call or a fixed workflow would do.
- No step, time, or cost budget, so the agent loops.
- Tools without schemas, permissions, or audit logs.
- Evaluating only the final answer, ignoring the trajectory and cost.

## Interview Notes

Expect "when do you need an agent vs a single call", "how do you stop infinite loops", "single vs
multi-agent", "how do you evaluate an agent". The strongest answer resists agents until simpler
options are proven insufficient.

## What You Should Know After Finishing

- The agent loop and the role of planning, tools, and memory.
- How to gate irreversible actions and set budgets and stop conditions.
- When a single agent beats a multi-agent design.
- How to evaluate trajectories, not just final answers.

## Suggested Exercises

- Design a meeting-booking agent: tools, stop conditions, the action that needs approval, three
  guardrails.
- Decide single vs multi-agent for a research task and justify it.
- List four production metrics for an agent and why each matters.
- Describe how you would detect and stop an agent stuck in a loop.

## Navigation

[🏠 Home](../README.md)
