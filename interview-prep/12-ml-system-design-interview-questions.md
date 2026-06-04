# ML System Design Interview Questions

## How to Use This File

Use this page to practice full-system ML design answers. A good answer must cover requirements,
data flow, model strategy, evaluation, serving, monitoring, reliability, privacy, and rollback. If
your answer only describes a model, it is incomplete.

For each prompt, speak in this order: clarify, requirements, data, baseline, architecture,
evaluation, production controls, tradeoffs. Draw a simple diagram while speaking if possible.

## Core Preparation Checklist

- Clarify users, scale, latency, freshness, permissions, and failure cost.
- Separate functional requirements from non-functional requirements.
- Define data sources, labels, feedback, ownership, and retention.
- Propose a baseline before advanced modeling.
- Separate offline training or indexing from online serving.
- Specify API inputs, outputs, model version, confidence, and audit identifiers.
- Include evaluation with primary metric, guardrails, slices, and hard examples.
- Add monitoring, alerts, rollback, canary release, human review, and incident ownership.
- Discuss privacy, security, fairness, and abuse risks where relevant.

## Interview Question Sections

### Question 1: Design a recommendation system for a marketplace.

**Strong answer:** Clarify whether the goal is clicks, purchases, retention, seller fairness, or
long-term satisfaction. Define candidate generation from popularity, collaborative filtering, and
content similarity, then ranking with user, item, context, freshness, and business features. Evaluate
with recall at k for candidates, NDCG or MRR for ranking, conversion and retention online, plus
guardrails for diversity, latency, fairness, and inventory health. Monitor drift, feedback loops,
cold start, and segment failures.

**Weak answer:** Train a collaborative filtering model and rank by predicted rating.

**Follow-up questions:**

- How do you handle new users and new items?
- How do you prevent popularity bias from dominating?
- What should be computed offline versus online?
- What metric would you not optimize alone?

**Common traps:** Ignoring candidate generation, optimizing short-term clicks only, and forgetting
feedback loops.

### Question 2: Design a fraud detection platform.

**Strong answer:** Clarify whether the output approves, blocks, challenges, or routes to review.
Define real-time features such as amount, merchant, device, account age, velocity, location, and
prior disputes. Start with rules and a calibrated tabular model, then consider graph or sequence
features. Evaluate fraud loss, false decline rate, review precision, recall at fixed friction budget,
latency, and fairness. Add human review, audit logs, rollback, and monitoring for new attack
patterns.

**Weak answer:** Train a classifier on past fraud and block every high score.

**Follow-up questions:**

- How do delayed chargeback labels affect training?
- What features are likely to leak?
- How do you handle adversarial adaptation?
- What happens when model confidence is low?

**Common traps:** Ignoring false declines, using future dispute data, and missing reviewer workflow.

### Question 3: Design a RAG platform for internal company knowledge.

**Strong answer:** Clarify corpus scope, user permissions, freshness, citation requirements, and
unanswerable questions. Design ingestion with parsing, chunking, metadata, embeddings, index
versioning, and deletion. Use permission-aware hybrid retrieval, reranking, and answer generation
that cites evidence and abstains when context is missing. Evaluate retrieval recall, context
precision, faithfulness, citation accuracy, latency, cost, and permission correctness.

**Weak answer:** Put documents into a vector database and ask an LLM to answer.

**Follow-up questions:**

- How do you handle permission changes?
- How do you evaluate retrieval separately from generation?
- What should happen with conflicting documents?
- How do you defend against prompt injection in retrieved text?

**Common traps:** Skipping access control, measuring only final answers, and assuming vector search
solves all retrieval.

### Question 4: Design a real-time inference platform.

**Strong answer:** Define model types, latency SLOs, traffic patterns, feature freshness, batch size,
fallback behavior, and model versioning. Separate feature computation, model serving, routing,
observability, and rollback. Include canary deployments, shadow traffic, autoscaling, timeout
budgets, cache strategy, circuit breakers, and monitoring for data drift, prediction drift, errors,
latency, and business outcomes.

**Weak answer:** Put the model behind an API endpoint.

**Follow-up questions:**

- What gets cached and what cannot be cached?
- How do you roll back a bad model?
- How do you detect train-serving skew?
- What happens when the feature store is unavailable?

**Common traps:** Forgetting timeouts, serving skew, model versioning, and operational ownership.

## Mini Exercise

Choose one system from `machine-learning-system-design/`. Draw the offline path and online path as
separate diagrams. Then write a five-minute answer with one baseline, one advanced approach, three
metrics, two failure modes, and one rollback plan.

## Diagram

```mermaid
flowchart LR
    A[Clarify requirements] --> B[Data contracts]
    B --> C[Offline training or indexing]
    C --> D[Online serving]
    D --> E[Evaluation]
    E --> F[Monitoring and rollback]
    F --> B
```

---
## Navigation

[⬅ Previous](11-agent-interview-questions.md) | [🏠 Home](../README.md) | [➡ Next](13-behavioral-ai-interviews.md)
