# Data Scientist Mock

## Round Format

This mock is a 60-minute interview round: 5 minutes for problem clarification, 15 minutes for
fundamentals, 20 minutes for design or modeling depth, 10 minutes for tradeoffs and failure modes,
and 10 minutes for self-review.

## Interviewer Prompt

Design or analyze a realistic system for the topic named in this mock. Explain the user problem,
baseline, data, model or architecture, evaluation, production risks, and improvement plan.

## Expected Clarification Questions

- Who is the user and what decision does the system support?
- What data is available at training time and serving time?
- What are the latency, cost, privacy, and reliability constraints?
- What mistakes are most expensive?
- How will success be measured online and offline?

## Expected Answer or Design

A strong answer starts with the product goal, defines the data and output, proposes a simple
baseline, chooses metrics tied to user impact, and then adds complexity only where justified. It also
covers error analysis, monitoring, rollback, human escalation, and tradeoffs.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Problem framing | Clear user, decision, constraints, and metric | Starts with a model name |
| Data reasoning | Mentions labels, splits, leakage, bias, and drift | Assumes data is clean |
| Modeling or design | Baseline first, complexity justified | Adds complexity without evidence |
| Evaluation | Uses task metrics and guardrails | Reports one generic score |
| Production | Covers monitoring, security, rollback, and ownership | Stops at notebook results |

## Red Flags

- No baseline.
- No leakage discussion.
- No primary metric or guardrail metric.
- No plan for low-confidence or unsafe outputs.
- No monitoring or rollback path.

## Self-Review Checklist

- Did I clarify the user and decision?
- Did I define data, labels, and constraints?
- Did I propose a baseline before an advanced approach?
- Did I explain metrics and failure modes?
- Did I include production operations and tradeoffs?

---
## Navigation

[⬅ Previous](03-llm-engineer-mock.md) | [🏠 Home](../README.md) | [➡ Next](05-rag-system-design-mock.md)
