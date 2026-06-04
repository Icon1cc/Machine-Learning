# Case Studies

## Folder Purpose

Applied ML and AI system case studies with product framing, requirements, data design, baselines,
advanced approaches, evaluation, scaling, reliability, security, observability, tradeoffs, and
interview scripts. This folder is where concepts become production-shaped design practice.

## Who Should Read This Section

Read this section when you need to practice the full reasoning loop rather than isolated concepts.
The case studies are useful for ML system design interviews, applied scientist discussions, capstone
planning, and senior-level review of tradeoffs.

This folder is especially useful if you can explain algorithms but struggle to answer:

- What exactly is the system deciding?
- What data is available at decision time?
- What baseline should ship first?
- Which failure mode is most expensive?
- How will the team know the system is getting worse?
- Where do privacy, permission, and human review enter the design?

## Recommended Reading Order

Read the first six studies to build classical ML and ranking instincts, then move into LLM, RAG,
vector search, monitoring, personalization, and agents. If you are preparing for interviews, do one
case study per day under a timer:

1. Spend five minutes clarifying requirements.
2. Spend ten minutes sketching data flow and baseline.
3. Spend ten minutes on evaluation, reliability, and risks.
4. Spend five minutes giving the interview explanation script out loud.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Spam Classifier](01-spam-classifier.md) |
| 2 | [Fraud Detection](02-fraud-detection.md) |
| 3 | [Credit Risk Model](03-credit-risk-model.md) |
| 4 | [Customer Churn Prediction](04-customer-churn-prediction.md) |
| 5 | [Recommendation System](05-recommendation-system.md) |
| 6 | [Search Ranking System](06-search-ranking-system.md) |
| 7 | [Ad Click Through Rate Prediction](07-ad-click-through-rate-prediction.md) |
| 8 | [Time Series Forecasting](08-time-series-forecasting.md) |
| 9 | [Document Classification](09-document-classification.md) |
| 10 | [Semantic Search Engine](10-semantic-search-engine.md) |
| 11 | [Chatbot With RAG](11-chatbot-with-rag.md) |
| 12 | [Enterprise Knowledge Assistant](12-enterprise-knowledge-assistant.md) |
| 13 | [Customer Support Agent](13-customer-support-agent.md) |
| 14 | [Code Assistant](14-code-assistant.md) |
| 15 | [AI Meeting Summarizer](15-ai-meeting-summarizer.md) |
| 16 | [LLM Evaluation Platform](16-llm-evaluation-platform.md) |
| 17 | [Vector Search At Scale](17-vector-search-at-scale.md) |
| 18 | [ML Monitoring Platform](18-ml-monitoring-platform.md) |
| 19 | [Personalization Engine](19-personalization-engine.md) |
| 20 | [AI Agent For Workflows](20-ai-agent-for-workflows.md) |

## What You Should Know After Finishing

- How to move from product problem to model decision without skipping requirements.
- How to separate functional requirements from non-functional requirements.
- How to choose a baseline that exposes data quality and evaluation problems early.
- How to reason about offline metrics, online metrics, guardrails, and hard-example sets.
- How to discuss scaling, reliability, security, observability, and human escalation in one coherent
  design.

## Case Study Review Checklist

For each case study, produce these artifacts:

- A one-paragraph product framing with user, decision, and consequence of a wrong answer.
- A data contract listing inputs, labels, feedback, freshness, and permission requirements.
- A baseline that could be implemented before advanced modeling.
- An evaluation plan with primary metric, guardrails, slices, and failure analysis.
- A production plan covering serving, monitoring, rollback, and ownership.
- A two-minute interview script that a non-specialist could follow.

## Suggested Exercises

- Redesign one case study for a low-latency product surface and again for a batch analytics surface.
- Add a failure-mode table to any study you find too optimistic.
- Compare a classical ML study with an LLM or agent study and list what changes in evaluation.
- Use one case study as the design basis for a capstone project and write the first project README.
- Practice explaining one study to a product manager, one to an ML engineer, and one to a security
  reviewer.

## Navigation

[🏠 Home](../README.md)
