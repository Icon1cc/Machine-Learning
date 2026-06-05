# Recommender Evaluation Metrics

## Beginner-Friendly Intuition

Evaluating a recommender system is harder than evaluating a classifier
because there is no single "right answer" per query. The user might
be interested in many items; not all relevant items get clicked; the
relevance judgment is subjective. Recommender metrics measure ranking
quality (did the top-K contain things the user wanted?) and
side-effects (was the recommendation list diverse enough? did the
system explore enough? did fairness hold?).

The intuition: pick metrics that match what your product cares about.
A retrieval stage cares about recall@K (did we surface relevant items
at all?). A ranker cares about NDCG@K (did we order them well?). A
business cares about online lift in the metric the company tracks
(watch time, retention, revenue), which is rarely the same as
offline metrics.

The biggest gotcha: offline-online gap. A model that wins offline by
2 NDCG points often produces zero or even negative online lift.
Reasons include position bias, distribution shift caused by changing
what the system shows, novelty effects, and the fact that offline
metrics use logged data from a different policy. Online A/B testing
is the decisive evaluation in production.

## Formal Explanation

### Offline metrics

Computed against a held-out set of (user, items_clicked) tuples.

#### Recall@K

```
Recall@K = | predicted_top_K ∩ relevant | / | relevant |
```

Of the items the user actually clicked, what fraction did we surface
in the top K? Used to measure retrieval (candidate generation).
Typical K: 100, 1000, 5000 for retrieval; 5, 10, 20 for ranking.

If retrieval has Recall@1000 = 0.85, the ranker can at best score
85 percent of relevant items; the missing 15 percent are gone.

#### Precision@K

```
Precision@K = | predicted_top_K ∩ relevant | / K
```

Of the items shown in the top K, what fraction was relevant? Often
secondary to recall; Precision@K shrinks as K grows even if quality
holds.

#### Mean Reciprocal Rank (MRR)

```
MRR = mean over queries of 1 / rank of first relevant item
```

If the first relevant item is at position 1, score is 1.0; at
position 5, score is 0.2; if not found, 0. Sensitive to top-1
quality. Useful when only the top result really matters (search
queries with a clear right answer).

#### Mean Average Precision (MAP)

```
AP_q = mean over relevant items of Precision@k_relevant
MAP = mean of AP over queries
```

Where `Precision@k_relevant` is the precision at the rank where each
relevant item appears. Rewards both precision and ranking order.

#### NDCG (Normalized Discounted Cumulative Gain)

```
DCG@K = Σ_{i=1..K} (2^rel_i - 1) / log2(i + 1)
NDCG@K = DCG@K / IDCG@K
```

Where `rel_i` is the relevance grade (often 1 for clicked, 0
otherwise; or 0-5 for graded relevance) and IDCG is the DCG of the
ideal ranking.

NDCG handles graded relevance (some items more relevant than others)
and discounts by position (later positions matter less). The standard
ranking metric for almost every recommender and search system.

#### Hit Rate@K

```
Hit Rate@K = fraction of users with at least one relevant item in top K
```

Binary: did we hit at all? Useful for cases where any relevant item
is enough.

#### Coverage

Fraction of items in the catalog that ever appear in any user's top
K recommendations. A model that recommends only the top 1 percent of
items has terrible coverage even if NDCG is high. Important for
long-tail and creator-side fairness.

#### Diversity

Within a single user's top K, how diverse are the items? Common
measures: intra-list distance (mean pairwise distance between
recommendations) or category entropy (Shannon entropy of category
distribution).

#### Novelty / Serendipity

Measures of how unexpected recommendations are. Novelty: how rare are
the items? Serendipity: how unexpected are they relative to the user's
history?

### Online metrics

The decisive evaluation. A/B test on real users.

- **Click-through rate (CTR).** Fraction of impressions that get
  clicked. Easy to game (clickbait); not always aligned with user
  satisfaction.
- **Conversion rate.** Fraction of impressions that lead to a
  purchase, signup, etc. Aligns with business outcome.
- **Watch time / dwell time.** For video and content. Measures
  engagement depth.
- **Retention.** Did the user come back tomorrow? In 7 days? In 30
  days? The most important metric for most products.
- **Long-term value.** Lifetime value, lifetime revenue. Slowest to
  measure; often replaced by short-term proxies.
- **Guardrail metrics.** Latency, error rate, complaint rate, opt-
  out rate. Even a recommender with great primary metrics is bad if
  guardrails regress.
- **Per-segment metrics.** New vs returning users, mobile vs desktop,
  geography. Aggregate metrics hide segment-specific failures.

### Counterfactual evaluation

Offline evaluation of a new policy using logs from the current
policy. Standard tool: **Inverse Propensity Score (IPS)** weighting.

```
IPS estimator: V(new policy) ≈ mean over logs of (new_score / log_score) · reward
```

The weight is the ratio of the new policy's probability of taking the
logged action to the logging policy's probability. With high variance
when the policies disagree heavily; many variants reduce variance
(self-normalized IPS, doubly robust estimators).

Used when running an A/B test is too expensive or risky; useful for
prefiltering candidate models before A/B.

### Offline-online gap

Why does offline NDCG often fail to predict online lift?

- **Distribution shift.** Logged data was collected under a different
  policy. The new policy shows different items, gets different
  feedback, may behave differently.
- **Position bias.** Items that appeared at position 1 got clicks
  that items at position 10 would also have gotten. Logged clicks are
  conflated with positions.
- **Novelty effect.** Users behave differently in the first week of
  a new model than in steady state. Offline metrics capture neither.
- **Selection bias.** The logged data has only items that were shown;
  unseen items have no data.
- **Multi-task interactions.** Optimizing one metric (watch time)
  often regresses others (retention).

Mitigations: position-bias correction in training, exploration to
gather data for the long tail, multi-week A/B tests, holdout
populations for long-term retention measurement.

### Common pitfalls in metric design

- **Random splitting on time-series data.** Recommender data is
  time-ordered; random split leaks future data into training. Use
  temporal split.
- **Ignoring repeat consumption.** A music recommender that
  recommends songs the user already loved might be the right answer
  even if they are "old" interactions.
- **Using accuracy.** Accuracy is for classification; for ranking,
  use NDCG / MAP / MRR.
- **Reporting only one metric.** Combine recall (retrieval),
  NDCG (ranking), and an online metric (CTR or watch time).

## Why It Matters in Real Jobs

Three production reasons. First, **wrong metric, wrong system**.
Optimizing CTR produces clickbait; optimizing watch time can produce
addiction-style content; optimizing retention is harder but aligns
better with long-term value. The metric chosen drives all
optimization. Second, **per-stage metrics for diagnosis**. When the
end-to-end metric drops, knowing which stage degraded (retrieval
recall? ranker NDCG? reranker policy?) is the difference between
fast fix and weeks of debugging. Third, **online-offline gap**
management. Investing in counterfactual evaluation and proper
position-bias handling reduces the rate of "model wins offline,
loses online" surprises.

## How It Works Step by Step

1. **Define the deployment metric.** What is the business win? Watch
   time, retention, revenue?
2. **Build proxy offline metrics.** Recall@K for retrieval, NDCG@K
   for ranking, plus diversity and coverage.
3. **Use temporal splits.** Train on past, evaluate on recent.
4. **Compute per-segment metrics.** Aggregate hides per-segment
   failures.
5. **Apply position-bias correction.** Logged data has position
   effects; train and evaluate accordingly.
6. **Run counterfactual evaluation** before A/B testing if available.
7. **A/B test.** The decisive evaluation.
8. **Monitor in production.** Per-stage metrics for diagnosis,
   end-to-end for decisions.
9. **Watch for novelty effects.** Run A/B tests for at least 1-2
   weeks to absorb day-of-week and novelty cycles.

## Real-World Example

A team improves their video ranker. Offline NDCG@10 rises from 0.41
to 0.46. They A/B test. Online watch time drops 2 percent. They
investigate.

- Per-segment analysis: power users see less watch time (-5
  percent); casual users see slight gains (+1 percent).
- Diversity analysis: the new ranker recommends fewer channels per
  user, increasing concentration on a few channels.
- Retention analysis: 7-day retention drops 1.5 percent.

The new ranker over-fits to short-term clicks at the cost of long-
term engagement. They add multi-task training (watch time + 7-day
retention as joint objective) and rerun. Offline NDCG@10 is 0.43
(slightly worse than the click-only ranker), but online watch time
is +1.5 percent and retention is +2 percent. They ship.

The lesson: offline NDCG was misleading; per-segment and longitudinal
metrics caught the real story.

## Common Mistakes

- Reporting only NDCG@10. Add Recall@K, diversity, per-segment.
- Using random splits on time-series recommender data; leakage
  inflates offline metrics.
- Ignoring position bias in offline evaluation; results are
  optimistic.
- Treating CTR as the goal; clickbait wins, retention loses.
- Skipping per-segment metrics; minorities (new users, rare
  segments) often regress invisibly.
- Running A/B tests for too short a period; novelty effects can flip
  the result.
- Skipping counterfactual evaluation; you A/B test bad models that
  could have been pruned offline.
- Not setting guardrail thresholds before launching; bad changes
  ship because nobody flagged them.
- Using popularity-biased relevance labels; the labels themselves
  reflect what the previous system showed.

## Interview Angle

**Question:** A team's new ranker improves offline NDCG@10 from 0.40
to 0.45. Online A/B test shows neutral watch time and a 2 percent
retention drop. What do you investigate?

**Strong answer:** The pattern (offline win, online flat or
regressed) is so common it has a name: the offline-online gap. Several
likely causes; the diagnostic is to investigate each in order.

1. **Per-segment analysis.** Aggregate metrics hide segment effects.
   New users, returning users, power users, mobile, desktop, country.
   Often the regression is concentrated in one segment that was hidden
   by gains elsewhere.

2. **Position bias.** The new ranker may be exploiting position effects
   in training data that do not transfer. Check whether position-bias
   correction was applied at training; verify the model does not just
   put high-CTR-by-position items at top regardless of relevance.

3. **Diversity collapse.** The new ranker may have higher NDCG by
   recommending more of the same. Compute intra-list diversity and
   per-creator coverage. If the new ranker reduces diversity, watch
   time can drop because users get bored or feel spammed.

4. **Distribution shift in candidates.** The new ranker may interact
   differently with the candidate generator. If candidate distribution
   changed, the ranker is operating in a different regime than offline.

5. **Multi-task trade-offs.** The new ranker may have over-optimized
   for clicks at the expense of long-term retention. Check if the
   model is multi-task; if so, examine the weights.

6. **Novelty effect.** Users may behave unusually in the first 1-2
   weeks of a new model (curiosity, confusion, loss of familiar
   items). Extend the A/B test for 4 weeks and watch for the trend
   to settle.

7. **Feedback loop.** The new ranker affects what items are shown,
   which affects what items get clicked, which is the next training
   data. The model may improve a metric in the short run that
   predicts a worse loop in the long run.

8. **Offline metric mismatch.** NDCG@10 might not correlate with the
   business metric the team cares about. Watch time is influenced by
   completion rate, click depth, return rate -- none of which is
   directly captured by NDCG.

The diagnostic procedure: pull per-segment metrics, diversity
metrics, multi-task target metrics, and the offline-online correlation
on past launches. The likely culprit is one of the above; iterate by
adding the missing target or correction.

The deeper takeaway: trust online metrics as the deployment criterion,
not offline metrics. Use offline as a filter for "obvious wins" and
"obvious losses"; require A/B tests for any launch.

**Weak answer:** "Trust the A/B test" without diagnosing why the
offline result misled.

**Follow-up questions:**

- What is position bias and how do you correct for it?
- What is a counterfactual evaluation?
- How would you measure long-term value online?
- Why is NDCG often the right offline metric?

## Mini Exercise

Take a small recommender dataset. Compute Recall@10, NDCG@10, MAP,
and MRR for two models (e.g., popularity vs collaborative filtering).
Note where they agree and disagree.

## Diagram

```mermaid
flowchart LR
    M[Model output] --> O{Metric type}
    O -- Retrieval --> R[Recall@K, Hit Rate]
    O -- Ranking --> N[NDCG@K, MAP, MRR]
    O -- Side --> S[Diversity, Coverage, Novelty]
    O -- Online --> A[CTR, Watch Time, Retention, Revenue]
    R --> Op[Operating decision]
    N --> Op
    S --> Op
    A --> Op
```

---
## Navigation

[⬅ Previous](06-candidate-generation-and-ranking.md) | [🏠 Home](../README.md) | [➡ Next](08-recommender-system-case-study.md)
