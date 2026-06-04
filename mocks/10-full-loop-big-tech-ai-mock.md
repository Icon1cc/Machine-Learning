# Full Loop Big Tech AI Mock

## Scenario

This simulates a full big-tech AI interview loop built around one product: "Design the ranking system
for a personalized home feed (think a social or content app) that serves billions of impressions per
day." The same product is stretched across the rounds a real loop contains: ML system design, a
modeling deep dive, coding, product sense, and behavioral.

## Round Format

A full loop, roughly 4 to 5 rounds of 45 to 60 minutes each:

1. **ML system design (60m):** end-to-end feed ranking architecture.
2. **Modeling deep dive (45m):** the ranking model, features, and training.
3. **Coding (45m):** implement a focused piece (for example, a top-k heap or a metrics function).
4. **Product sense (45m):** what to optimize and how to measure feed quality.
5. **Behavioral (45m):** ownership, conflict, and a project you drove.

## Interviewer Prompt

Across rounds, the loop tests whether you can design a large-scale system, justify modeling choices,
write correct code, reason about product metrics, and communicate like a senior engineer. Keep one
coherent story from product goal to production.

## Expected Clarification Questions

- What is the objective: engagement, long-term retention, or a balance with creator and integrity
  goals?
- What is the candidate pool size per request and the latency budget?
- What signals are available (interactions, content features, social graph, freshness)?
- How do we avoid feedback loops and filter bubbles?
- What are the integrity constraints (no harmful or low-quality content amplified)?

## Expected Answer or Design

A strong candidate keeps a two-stage architecture front and center: cheap candidate generation
(retrieval from follows, embeddings, and trending) narrows millions to hundreds, then a heavier
ranking model scores those, then a re-ranking layer applies diversity, freshness, and integrity
rules. Training uses logged interactions with care for position bias and the fact that you only
observe feedback on items you showed. The objective is multi-task (clicks, dwell, long-term value
proxies) rather than raw clicks, because optimizing clicks alone degrades the product.

Evaluation spans offline (NDCG, calibration) and online (A/B tests on retention and satisfaction, not
just CTR), with guardrails on integrity and creator diversity. Production: precompute embeddings,
serve ranking under the latency budget, monitor for drift and feedback loops, and roll out via
experiments. In the modeling round, go deep on features and the multi-task loss. In coding, implement
the top-k selection cleanly with correct complexity. In product sense, argue for long-term metrics
over vanity clicks. In behavioral, show ownership of a real tradeoff.

## Worked Strong Answer Outline

1. Two stages: candidate generation then ranking then re-rank for diversity and integrity.
2. Multi-task objective (not pure CTR) to protect long-term value.
3. Handle position bias and the "only see what you showed" feedback problem.
4. Offline NDCG and calibration; online A/B on retention with integrity guardrails.
5. Precompute embeddings, serve under budget, monitor feedback loops and drift.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| System design | Two-stage retrieval + ranking + re-rank | One giant model scores everything |
| Modeling | Multi-task objective, position bias handled | Optimizes raw clicks |
| Coding | Correct, efficient top-k with clear complexity | Buggy or brute-force only |
| Product sense | Long-term metrics and integrity guardrails | "Maximize engagement" with no nuance |
| Communication | One coherent story across rounds | Disconnected, contradictory answers |

## Red Flags

- Scoring millions of candidates with one heavy model (no candidate generation).
- Optimizing clicks alone and ignoring long-term and integrity effects.
- Ignoring position bias and the partial-feedback problem.
- Measuring only CTR, never retention or satisfaction.
- Coding that is incorrect or ignores complexity at this scale.

## Follow-Up Questions

- Engagement rose but weekly retention fell after launch. What did you optimize wrong?
- The feed shows the same creators repeatedly. How do you fix diversity without hurting relevance?
- Implement top-k selection from a stream and state the time and space complexity.

## Self-Review Checklist

- Did I keep one coherent product story across all rounds?
- Did I use a two-stage retrieval-then-ranking design?
- Did I choose a multi-task objective and handle position bias?
- Did I evaluate with long-term online metrics and integrity guardrails?
- Did I write correct, efficient code and communicate tradeoffs clearly?

---
## Navigation

[⬅ Previous](09-mlops-mock.md) | [🏠 Home](../README.md) | [➡ Next](../quizzes/01-ml-fundamentals-quiz.md)
