# Recommender Systems

## Folder Purpose

Candidate generation, ranking, collaborative filtering, matrix factorization, and recommender evaluation.

## Beginner Intuition

A recommender predicts what a user will want next from what they and similar users did before. At
scale you cannot score every item for every user, so the standard shape is two stages: cheaply
generate a few hundred candidates, then rank them with a heavier model, then re-rank for diversity and
freshness.

## Why It Matters

Feeds, product suggestions, and "you might also like" drive a large fraction of engagement and revenue
at consumer companies. Recommenders are also a favorite ML system design interview because they force
you to reason about scale, latency, cold start, and feedback loops.

## Who Should Read This Section

Read this if you target consumer-ML or ranking roles, or want a canonical large-scale system to
practice. It connects to the vector-database, deep-learning, and system-design sections.

## Recommended Reading Order

Read in order: overview, collaborative and content-based filtering, matrix factorization, ranking,
the two-stage candidate-generation-and-ranking design, evaluation, then the case study.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Recommender Systems Overview](01-recommender-systems-overview.md) |
| 2 | [Collaborative Filtering](02-collaborative-filtering.md) |
| 3 | [Content Based Filtering](03-content-based-filtering.md) |
| 4 | [Matrix Factorization](04-matrix-factorization.md) |
| 5 | [Ranking Systems](05-ranking-systems.md) |
| 6 | [Candidate Generation And Ranking](06-candidate-generation-and-ranking.md) |
| 7 | [Evaluation Metrics](07-evaluation-metrics.md) |
| 8 | [Recommender System Case Study](08-recommender-system-case-study.md) |

## Real-World Examples

- A video feed: candidate generation from follows and embeddings, then a ranking model on engagement.
- E-commerce "customers also bought" from collaborative filtering on co-purchase data.
- Music discovery blending content features (audio) with collaborative signals.
- News ranking that must balance relevance with freshness and diversity.

## Pattern Recognition

- "Score millions of items in milliseconds" points to two-stage retrieval then ranking.
- "New user or item with no history" points to the cold-start problem and content features.
- "Optimized clicks but users left" points to a feedback loop and the wrong objective.
- "Always shows the same few items" points to missing diversity or popularity bias.

## Common Mistakes

- Trying to rank the full catalog with one heavy model (no candidate generation).
- Optimizing raw clicks instead of long-term value, which degrades the product.
- Ignoring cold start for new users and items.
- Evaluating offline only and skipping an online test of retention.

## Interview Notes

Expect "design a recommendation feed", "collaborative vs content-based", "how do you handle cold
start", "what metric". Use NDCG and recall@k offline, retention and satisfaction online, and always
mention the two-stage architecture.

## What You Should Know After Finishing

- The two-stage candidate-generation-then-ranking architecture.
- Collaborative vs content-based filtering and matrix factorization.
- How to handle cold start and popularity bias.
- Offline (NDCG, recall@k) vs online (retention) evaluation.

## Suggested Exercises

- Sketch a two-stage recommender for a video app with latency budgets.
- Propose a cold-start strategy for brand-new items.
- Explain why optimizing clicks alone can hurt retention.
- Choose offline and online metrics for a shopping feed and justify them.

## Navigation

[🏠 Home](../README.md)
