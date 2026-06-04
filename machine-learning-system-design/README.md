# Machine Learning System Design

## Folder Purpose

System design practice for ML platforms, recommendation systems, search ranking, fraud detection,
feature stores, RAG, agents, LLM evaluation, real-time inference, and AI copilots. This folder helps
you design systems where models are only one part of a larger product and operations loop.

## Who Should Read This Section

Use this section when a prompt requires architecture, data flow, evaluation, serving, reliability,
and ownership. It is for learners who can describe a model but need practice turning that model into
a production system with clear interfaces and tradeoffs.

This folder is especially useful for ML Engineer, AI Engineer, LLM Engineer, and senior Data
Scientist interviews where the interviewer expects both ML judgment and distributed-system judgment.

## Recommended Reading Order

Read 01 through 05 first to build classical ML system design instincts. Then read 06 through 08 for
RAG, agents, and evaluation systems. Finish with 09 and 10 for latency-sensitive serving and
assistant-style products.

For interview practice, repeat this structure for every design:

1. Clarify users, product goal, scale, latency, privacy, and failure cost.
2. Define data sources, labels, feedback, freshness, and permissions.
3. Propose a baseline and a more advanced path.
4. Design offline training or indexing and online serving separately.
5. Specify evaluation, monitoring, rollback, and human review.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Design A Recommendation System](01-design-a-recommendation-system.md) |
| 2 | [Design A Search Ranking System](02-design-a-search-ranking-system.md) |
| 3 | [Design A Fraud Detection Platform](03-design-a-fraud-detection-platform.md) |
| 4 | [Design An ML Training Platform](04-design-an-ml-training-platform.md) |
| 5 | [Design A Feature Store](05-design-a-feature-store.md) |
| 6 | [Design A RAG Platform](06-design-a-rag-platform.md) |
| 7 | [Design An Agent Platform](07-design-an-agent-platform.md) |
| 8 | [Design An LLM Evaluation System](08-design-an-llm-evaluation-system.md) |
| 9 | [Design A Real Time Inference System](09-design-a-real-time-inference-system.md) |
| 10 | [Design An AI Copilot Platform](10-design-an-ai-copilot-platform.md) |

## What You Should Know After Finishing

- How to turn an ambiguous ML product prompt into requirements and constraints.
- How to draw data flow from ingestion through features, training, evaluation, serving, and feedback.
- How to choose between batch, streaming, online inference, retrieval, reranking, and human review.
- How to connect offline metrics to online guardrails and operational alerts.
- How to discuss scale, cost, latency, privacy, fairness, explainability, and rollback without losing
  the main product goal.

## Design Review Checklist

Before calling an answer complete, verify that it includes:

- Functional requirements and non-functional requirements.
- Data contracts and label or feedback collection.
- Baseline, advanced approach, and why complexity is justified.
- API or serving contract with versioning and auditability.
- Evaluation plan with slices, guardrails, and hard examples.
- Monitoring, rollback, ownership, and incident response.
- Security and privacy boundaries.

## Suggested Exercises

- Redesign one system for ten times the traffic and list what changes first.
- For each file, write the offline path and online path as separate bullet lists.
- Pair one design with a case study and one capstone project.
- Practice a five-minute answer, then a thirty-minute answer, for the same prompt.
- After every design, identify one decision you would validate with an experiment or prototype.

## Navigation

[🏠 Home](../README.md)
