# LLM Evaluation Platform

## Problem Statement

Build an llm evaluation platform for LLM quality measurement. The system uses test prompts, expected criteria, model outputs, judge rubrics, traces, and human ratings to support this output:
scorecards, regressions, failure clusters, and release recommendations. Treat the case as an interview design exercise and a production review: define the
decision, start with a baseline, measure quality honestly, and explain how the system behaves when
confidence is low.

## Domain Context

In this domain, the model is part of an operational decision. A strong design makes the cost of a
wrong output explicit, defines what data is available at decision time, and explains how the system
will recover when confidence is low. The highest-risk failure to plan around is shipping a model change because the evaluation set missed a critical workflow.

## Functional Requirements

- Ingest test prompts, expected criteria, model outputs, judge rubrics, traces, and human ratings.
- Produce scorecards, regressions, failure clusters, and release recommendations.
- Provide confidence, evidence, or explanation when the workflow needs it.
- Support human review for low-confidence or high-risk outputs.
- Capture feedback so the system can be evaluated and improved.

## Non-Functional Requirements

- Meet latency expectations for the product surface.
- Keep data access, privacy, and retention rules explicit.
- Provide reproducible training or evaluation runs.
- Support monitoring, alerting, rollback, and ownership.
- Degrade gracefully when dependencies or model outputs fail.

## Assumptions

- Historical examples or documents are available for baseline development.
- Labels, outcomes, or human judgments can be collected for evaluation.
- The first version should prioritize measurable reliability over model complexity.
- Deployment traffic may differ from development data.

## Data Assumptions

- Inputs are timestamped so training, validation, and serving windows can be separated.
- Sensitive fields are minimized, redacted, or access-controlled before modeling.
- Labels or judgments have known delay, noise, and reviewer disagreement.
- Feedback can be joined back to model versions, prompts, features, or retrieval indexes.

## Architecture Diagram

```mermaid
flowchart LR
    A[Product request] --> B[Input validation]
    B --> C[Feature, chunk, or context pipeline]
    C --> D[Baseline]
    C --> E[Advanced approach]
    D --> F[Offline evaluation]
    E --> F
    F --> G[Serving or workflow layer]
    G --> H[Monitoring, feedback, and review]
    H --> C
```

## Data Model or Data Design

Track raw inputs, normalized features or chunks, labels or judgments, model outputs, confidence
scores, timestamps, entity identifiers, and feedback events. Include version fields for features,
models, prompts, retrieval indexes, and evaluation datasets so offline results can be compared with
production behavior.

## API Design

A minimal production API should accept the domain input, return the output, confidence, model
version, explanation or evidence when needed, and an audit identifier for tracing. Batch jobs should
produce the same logical fields in a versioned artifact so results can be replayed and inspected.

## Baseline Approach

Start with golden test sets with deterministic string and rubric checks. The baseline should be easy to explain, cheap to run, and strong enough to
expose data quality problems before advanced modeling begins.

## Advanced Approach

After measuring the baseline, consider LLM-as-judge with calibration, pairwise comparison, and trace-level diagnostics. Add complexity only when it improves a named
metric or reduces a known operational risk.

## Model Choices

| Option | When it fits | Main risk |
| --- | --- | --- |
| Rules or search baseline | The workflow needs explainability and fast iteration | Can miss nuanced patterns |
| Classical model | Tabular or sparse features carry strong signal | Can leak features or underfit complex behavior |
| Deep model or LLM workflow | Text, images, retrieval, or reasoning dominate the task | Higher latency, cost, and evaluation burden |
| Human review | Errors are costly or confidence is low | Review capacity can become the bottleneck |

## Evaluation Plan

Evaluate with judge agreement, regression detection, coverage, false alarm rate, and evaluation cost. Include slice analysis for important user, item, time, source, language, or
risk segments. Keep a small set of hard examples for regression checks and review disagreements
between model outputs and human judgment.

## Metrics and Guardrails

| Metric Type | Examples |
| --- | --- |
| Primary quality | judge agreement, regression detection, coverage, false alarm rate, and evaluation cost |
| Guardrail | Latency, cost, privacy incidents, unsafe actions, and user complaints |
| Data quality | Missing fields, stale inputs, label delay, and source coverage |
| Operations | Error rate, timeout rate, review backlog, rollback count, and alert response time |

## Scaling Strategy

Separate offline processing from online serving, cache stable computations, precompute embeddings or
features where possible, and define data freshness requirements. Use batch, streaming, or online
inference based on latency and consistency needs.

## Reliability Strategy

Use validation checks, fallback responses, timeouts, retries with limits, canary releases, rollback
plans, and human escalation for high-risk cases. Monitor both technical health and output quality.

## Security Considerations

Limit access to sensitive inputs, redact private fields where possible, enforce authorization before
retrieval or prediction, log only what is necessary, and review prompt or tool injection risks for
LLM workflows.

## Observability

Capture input distributions, model version, prompt or retrieval version, latency, cost, errors,
confidence, decision outcomes, and human feedback. Use dashboards and alerts tied to user impact.

## Bottlenecks

Common bottlenecks include slow feature generation, expensive model calls, poor retrieval recall,
manual labeling throughput, delayed ground truth, and noisy feedback loops.

## Failure Modes

- The system optimizes an offline metric that does not match the product decision.
- Feedback loops reinforce early mistakes or popular items.
- A data pipeline change silently shifts feature values or retrieval quality.
- Confidence is poorly calibrated, causing the system to automate cases that need review.
- The critical failure to plan around is shipping a model change because the evaluation set missed a critical workflow.

## Tradeoffs

- Simplicity versus model quality.
- Latency versus richer context or larger models.
- Precision versus recall or relevance depth.
- Automation versus human review.
- Freshness versus reproducibility.

## Interview Explanation Script

I would start by clarifying the decision this system supports, the available data, and the cost of
shipping a model change because the evaluation set missed a critical workflow. Then I would build golden test sets with deterministic string and rubric checks, define metrics around judge agreement, regression detection, coverage, false alarm rate, and evaluation cost, inspect errors by segment,
and only then consider LLM-as-judge with calibration, pairwise comparison, and trace-level diagnostics. For production, I would add monitoring, fallback behavior, privacy
review, and a feedback loop before increasing automation.

## Follow-Up Questions

- What baseline would you build first?
- How would you prevent leakage?
- Which metric matters most and which metrics are guardrails?
- What happens when confidence is low?
- How would the design change at ten times the traffic?

## Common Mistakes

- Starting with an advanced model before defining the decision and metric.
- Ignoring delayed labels, missing data, or leakage.
- Reporting one aggregate score without segment analysis.
- Forgetting monitoring, rollback, security, and ownership.
- Treating offline performance as proof of production reliability.

---
## Navigation

[⬅ Previous](15-ai-meeting-summarizer.md) | [🏠 Home](../README.md) | [➡ Next](17-vector-search-at-scale.md)
