# MLOps

## Folder Purpose

Reproducibility, experiment tracking, model registries, serving, monitoring, CI/CD, and governance.

## Beginner Intuition

MLOps is what keeps a model useful after the notebook. A model is not done when it trains well; it is
done when it can be reproduced, deployed, monitored, and retrained safely. The recurring theme is
versioning everything (data, features, code, model) so any prediction can be traced and any regression
rolled back.

## Why It Matters

Models decay. The world shifts, inputs change, and yesterday's accuracy is no guarantee. Without drift
monitoring and a retraining trigger, you learn about failure from angry users, not dashboards. Most
production ML incidents are MLOps gaps, not modeling mistakes.

## Who Should Read This Section

Read this if you deploy models, own them in production, or interview for ML-engineer and ML-platform
roles. It is the operational backbone under everything else in the curriculum.

## Recommended Reading Order

Read in order: what MLOps is, then reproducibility and versioning, experiment tracking, feature
stores, registries, serving, batch vs online, monitoring and drift, CI/CD, governance, and finally ML
system design.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is MLOps](01-what-is-mlops.md) |
| 2 | [Reproducibility](02-reproducibility.md) |
| 3 | [Data Versioning](03-data-versioning.md) |
| 4 | [Experiment Tracking](04-experiment-tracking.md) |
| 5 | [Feature Stores](05-feature-stores.md) |
| 6 | [Model Registries](06-model-registries.md) |
| 7 | [Model Serving](07-model-serving.md) |
| 8 | [Batch Vs Online Inference](08-batch-vs-online-inference.md) |
| 9 | [Monitoring Drift And Alerting](09-monitoring-drift-and-alerting.md) |
| 10 | [CI CD For ML](10-ci-cd-for-ml.md) |
| 11 | [Model Governance](11-model-governance.md) |
| 12 | [ML System Design](12-ml-system-design.md) |

## Real-World Examples

- A fraud model whose catch rate decays for months because nobody monitored drift.
- A feature store that serves identical features offline and online, killing training/serving skew.
- A model registry with staging and production stages enabling a one-step rollback.
- A drift alert (PSI on inputs) that triggers an automated retrain and validation gate.

## Pattern Recognition

- "It worked at launch, then quietly got worse" points to missing drift monitoring.
- "Cannot reproduce the result" points to unversioned data or code.
- "Offline great, online bad" points to training/serving skew.
- "We retrain on a schedule" with no trigger or gate points to wasted compute and risk.

## Common Mistakes

- Treating deployment as the finish line, with no monitoring.
- Shipping from a notebook with no versioning, so rollback is impossible.
- Computing features differently online and offline.
- Retraining without a validation gate before promotion.

## Interview Notes

Expect "how do you monitor a model in production", "data drift vs concept drift", "batch vs online
inference", "what is a feature store and why". Name the failure mode and the specific control that
catches it.

## What You Should Know After Finishing

- What to version so a prediction is reproducible and reversible.
- The difference between data drift and concept drift and how to detect each.
- When to use batch, online, or streaming inference.
- How monitoring, alerts, and a retraining trigger fit together.

## Suggested Exercises

- Design the lifecycle for a weekly-retrained model: version, monitor, trigger, gate, rollback.
- Explain how a feature store removes training/serving skew.
- For a model with labels delayed by weeks, list what you monitor on day one.
- Describe a canary deploy and how it limits the blast radius of a bad model.

## Navigation

[🏠 Home](../README.md)
