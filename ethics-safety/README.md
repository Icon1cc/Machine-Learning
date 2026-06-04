# Ethics Safety

## Folder Purpose

Fairness, privacy, security risks, misuse, responsible AI, and governance.

## Beginner Intuition

ML systems make decisions about people, so they can be unfair, leak private data, be misused, or be
attacked. Ethics and safety is the discipline of finding those harms before they happen and building
controls so the system fails safely. It is not a compliance afterthought; it is part of correct
engineering.

## Why It Matters

A model that is accurate on average can still systematically harm a subgroup, expose personal data, or
be jailbroken into producing dangerous content. These failures carry legal, reputational, and human
costs that dwarf a few accuracy points. Senior interviews increasingly probe whether you think about
this by default.

## Who Should Read This Section

Read this if you ship models that touch people, handle sensitive data, or interview for roles where
responsible-AI judgment matters. It connects to the production-AI, agents, and LLM sections.

## Recommended Reading Order

Read in order: ethics overview, then bias and fairness, privacy, security risks, misuse, responsible
AI practice, and governance, which ties the controls into an accountable process.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [AI Ethics Overview](01-ai-ethics-overview.md) |
| 2 | [Bias And Fairness](02-bias-and-fairness.md) |
| 3 | [Privacy](03-privacy.md) |
| 4 | [Security Risks](04-security-risks.md) |
| 5 | [Model Misuse](05-model-misuse.md) |
| 6 | [Responsible AI](06-responsible-ai.md) |
| 7 | [AI Governance](07-ai-governance.md) |

## Real-World Examples

- A hiring model that down-ranks a protected group because of biased historical data.
- A model that memorizes and leaks training data containing personal information.
- An LLM jailbroken past its safety filters to produce harmful instructions.
- A facial-recognition system deployed without consent or accuracy review across skin tones.

## Pattern Recognition

- "Accurate overall but worse for group X" points to a fairness and disparate-impact problem.
- "The model repeats training text verbatim" points to a privacy and memorization risk.
- "Users can trick it into unsafe output" points to security and jailbreak defenses.
- "Nobody owns the decision" points to a governance gap.

## Common Mistakes

- Measuring only aggregate accuracy and never slicing by protected group.
- Collecting and retaining personal data with no minimization or consent.
- Treating safety filters as solved instead of continuously tested.
- Deploying high-impact decisions with no human appeal or oversight.

## Interview Notes

Expect "how would you check a model for bias", "what privacy risks does this system have", "how do you
defend against misuse". Strong answers name the specific harm, the way to measure it, and the control
that mitigates it.

## What You Should Know After Finishing

- How to detect and mitigate bias across subgroups.
- The main privacy risks (PII, memorization, retention) and defenses.
- Common security and misuse threats and guardrails.
- How governance assigns ownership and accountability.

## Suggested Exercises

- Design a fairness audit for a lending model, including the slices you would check.
- List the privacy controls for a system that handles user messages.
- Describe two jailbreak risks for an LLM and a defense for each.
- Sketch a governance process: who approves, who monitors, who is accountable.

## Navigation

[🏠 Home](../README.md)
