# ML Engineer Mock

## Scenario

You are interviewing for an ML Engineer role. The prompt: "Design the click-through-rate (CTR)
prediction service for our ad ranking system. It must score candidate ads in under 20 ms at the 95th
percentile and handle around 50,000 queries per second at peak."

## Round Format

A 60-minute round: 5 minutes clarifying the ranking context, 15 minutes on features and model, 20
minutes on the serving architecture and latency budget, 10 minutes on training, evaluation, and
drift, and 10 minutes on failure modes and rollout.

## Interviewer Prompt

This is a high-throughput, low-latency modeling and systems problem. Cover the label, the features
and where they come from, the model family, how you hit the latency budget, how you train and
evaluate, and how you keep the model fresh.

## Expected Clarification Questions

- What is the label and how delayed is it (a click within what attribution window)?
- Are we ranking a fixed candidate set per request, and how many ads per request?
- Where do features live: request context, precomputed user/ad features, or both?
- What is the retraining cadence and how fast does ad inventory change?
- Is the business metric CTR, revenue per impression, or a long-term value proxy?

## Expected Answer or Design

A strong candidate separates offline training from online serving and respects the latency budget.
Label: click within an attribution window, with care that non-clicks are not all true negatives.
Features: dense user and ad features precomputed and fetched from a low-latency store (the feature
store), plus cheap request-context features computed inline. Model: gradient-boosted trees or a
compact DNN/wide-and-deep; the key is that embeddings and heavy features are precomputed so the
online path is a fast lookup plus a small forward pass.

Latency: batch the candidate ads into one vectorized scoring call, precompute user embeddings offline,
cache hot features, and keep the model small enough to score hundreds of ads in the budget.
Evaluation: offline AUC and log-loss with calibration (CTR feeds bidding, so calibrated probabilities
matter), then online A/B on revenue and CTR with guardrails on latency and ad quality. Drift: CTR
shifts fast, so retrain daily or hourly and monitor calibration and feature distributions.

## Worked Strong Answer Outline

1. Split offline training from online serving; the online path must be a lookup plus a tiny model.
2. Precompute user and ad embeddings; fetch from a feature store with strict p95.
3. Calibrated probabilities matter because CTR feeds the bid, not just ranking.
4. Batch-score all candidates per request in one vectorized call.
5. Retrain frequently; monitor calibration drift and feature skew.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Label reasoning | Handles attribution window and negative sampling | Assumes clean binary labels |
| Features | Precompute heavy, compute light inline, feature store | Computes everything online |
| Serving | Hits p95 budget with batching and caching | Ignores the 20 ms constraint |
| Evaluation | Calibration + online A/B on revenue | Reports only AUC |
| Freshness | Frequent retrain, drift and skew monitoring | Trains once, never updates |

## Red Flags

- Ignoring the 20 ms p95 and 50k QPS constraints.
- Treating all non-clicks as negatives without sampling reasoning.
- No calibration despite probabilities feeding bidding.
- Training/serving skew from features computed differently offline and online.
- No retraining or drift plan for a fast-moving distribution.

## Follow-Up Questions

- p95 latency is 35 ms, over budget. What is your first optimization?
- Offline AUC improved but online revenue dropped. What happened?
- A new ad has no history. How do you score it (cold start)?

## Self-Review Checklist

- Did I separate offline training from the online serving path?
- Did I respect the latency and throughput budget concretely?
- Did I address label delay and negative sampling?
- Did I mention calibration and an online revenue test?
- Did I cover drift, retraining, and training/serving skew?

---
## Navigation

[⬅ Previous](01-ai-engineer-mock.md) | [🏠 Home](../README.md) | [➡ Next](03-llm-engineer-mock.md)
