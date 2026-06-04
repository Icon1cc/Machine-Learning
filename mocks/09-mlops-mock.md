# MLOps Mock

## Scenario

You are interviewing for an MLOps or ML platform role. The prompt: "Our fraud model performed well at
launch, but over three months its catch rate quietly dropped and chargebacks rose. Nobody noticed
until finance flagged it. Design the system so this never happens silently again, and so we can
recover fast when a model goes bad."

## Round Format

A 60-minute round: 5 minutes clarifying the current gaps, 15 minutes on monitoring design, 20 minutes
on retraining and the registry, 10 minutes on rollback and safe deploys, and 10 minutes on
ownership and alerting.

## Interviewer Prompt

This is an MLOps reliability problem. The model is fine; the lifecycle around it is broken. Cover
monitoring (including delayed labels), drift detection, retraining triggers, versioning, rollback,
and who gets paged.

## Expected Clarification Questions

- How delayed are fraud labels (chargebacks can take weeks), and how do we monitor before they
  arrive?
- Is the model versioned and reproducible today, or did it ship from a notebook?
- Do features come from a shared store, or are they recomputed at serving time?
- What is the cost of a missed fraud case versus a false decline?
- Who currently owns the model in production, and is anyone on call?

## Expected Answer or Design

A strong candidate separates two monitoring layers because labels are delayed. Leading indicators
(available immediately): input feature drift (PSI, KS tests), score distribution shift, and decline
rate. Lagging indicators (weeks later): actual catch rate and chargeback rate once labels resolve.
Both feed alerts with thresholds, and someone is on call. The silent failure happened because only
offline launch metrics existed and no one watched drift.

Recovery requires versioning: data, features, code, and model all pinned, with models in a registry
gated by a validation step before promotion. Deploys go out as canary or shadow first, so a bad model
is caught on a slice before full traffic. Rollback is a one-step revert to the previous registered
version. Retraining is triggered by drift alerts and a scheduled cadence, always passing the
validation gate before promotion. A feature store kills training/serving skew. The end state: drift is
caught in days not months, a bad model rolls back in minutes, and a named owner is paged on breach.

## Worked Strong Answer Outline

1. Two monitoring layers: leading (drift, score shift) and lagging (catch rate, chargebacks).
2. Alerts with thresholds and a named on-call owner.
3. Version data, features, code, model; promote through a registry with a gate.
4. Canary or shadow deploys; one-step rollback.
5. Retrain on drift trigger plus cadence; feature store removes skew.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Monitoring | Leading and lagging metrics with delayed labels | Only offline launch metrics |
| Drift | PSI/KS on features and scores | "We will check accuracy sometimes" |
| Versioning | Data + feature + code + model, registry | Notebook-shipped, unversioned |
| Rollback | Canary/shadow, one-step revert | No rollback path |
| Ownership | Named owner, on-call, alert thresholds | Nobody is paged |

## Red Flags

- Relying only on offline launch metrics with no production monitoring.
- No plan for delayed labels (monitoring nothing until chargebacks resolve).
- No model or data versioning, so rollback is impossible.
- Promoting models with no validation gate.
- No owner, no on-call, no alert thresholds.

## Follow-Up Questions

- Labels take three weeks. What do you watch on day one to catch a bad model?
- A drift alert fires but the model is actually fine (a legit traffic shift). How do you avoid alert
  fatigue?
- Retraining made things worse. How does your gate and rollback handle that?

## Self-Review Checklist

- Did I design monitoring for both leading and lagging signals?
- Did I account for delayed fraud labels?
- Did I version data, features, code, and model with a registry?
- Did I include canary deploys and one-step rollback?
- Did I assign ownership, on-call, and alert thresholds?

---
## Navigation

[⬅ Previous](08-deep-learning-mock.md) | [🏠 Home](../README.md) | [➡ Next](10-full-loop-big-tech-ai-mock.md)
