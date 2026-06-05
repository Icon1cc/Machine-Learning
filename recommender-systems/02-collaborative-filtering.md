# Collaborative Filtering

## Beginner-Friendly Intuition

Collaborative filtering recommends items based on what similar users
liked. The simplest version: find users similar to me, look at what
they bought that I have not, recommend those. The "collaboration" is
implicit: I benefit from the choices other users made, without anyone
explicitly comparing notes.

The intuition for why it works: behavior reveals taste. Two users who
both watched the same 50 obscure movies probably share taste in a 51st.
The pattern of co-occurrence in user-item interactions is a strong
signal even when you have no information about why people liked
those items. Collaborative filtering was the first major recommender
system technique (Amazon, 1990s) and remains a strong baseline.

The two flavors: **user-based** ("users like you bought") and **item-
based** ("items similar to ones you bought"). Item-based dominated
production through the 2000s because it scales better; both have been
largely replaced by matrix factorization and deep retrieval, but their
intuition still grounds modern systems.

## Formal Explanation

### Setup

Build the user-item interaction matrix `R`:

```
R[u, i] = 1 if user u interacted with item i
        = 0 otherwise
```

(For explicit ratings, `R[u, i]` is the rating value; for implicit
feedback, it is the click/purchase indicator.)

### User-based collaborative filtering

To recommend for user `u`:

1. Compute similarity between `u` and every other user. Common
   measures: cosine similarity, Pearson correlation, Jaccard.
2. Pick the top-K most similar users (the neighborhood).
3. For each item `i` not interacted with by `u`, predict a score
   based on the neighbors' interactions:

```
score(u, i) = Σ_{v ∈ neighbors} sim(u, v) · R[v, i] / Σ |sim(u, v)|
```

4. Recommend the top-scoring items.

### Item-based collaborative filtering

To recommend for user `u`:

1. Compute similarity between every pair of items. Cosine of the
   item columns of `R` is the standard.
2. For each item `i` not interacted with by `u`, predict a score
   based on `u`'s past items:

```
score(u, i) = Σ_{j ∈ u's items} sim(i, j) · R[u, j] / Σ |sim(i, j)|
```

3. Recommend the top-scoring items.

Item-based is preferred in production because the item-item similarity
matrix can be precomputed and is more stable than user similarity
(items change rarely; users often).

### Similarity functions

For implicit feedback (binary):

- **Jaccard.** `|A ∩ B| / |A ∪ B|`.
- **Cosine.** Treat the column as a binary vector and compute cosine.

For explicit ratings:

- **Pearson correlation.** Standardize ratings; cosine on standardized.
- **Adjusted cosine.** Subtract user mean before cosine.

### Implicit vs explicit feedback

- **Explicit feedback.** User-given ratings (1-5 stars). Sparse,
  biased toward extremes, not always available.
- **Implicit feedback.** Clicks, purchases, watch time, dwell time.
  Far more abundant than ratings; what every modern system uses.

The implicit feedback has known issues. The 0 entry can mean "did not
like" or "did not see"; modern methods (BPR, weighted matrix
factorization) handle this with confidence weights or pairwise
comparisons.

### Strengths

- **Simple and interpretable.** "People who bought this also bought"
  is human-readable.
- **No item features needed.** Works on items with only an ID, no
  metadata.
- **Captures non-obvious preferences.** Co-occurrence patterns can
  reveal niche tastes that content-based filtering misses.
- **Strong baseline.** A well-tuned item-based CF system often beats
  fancier models for moderate-data settings.

### Weaknesses

- **Cold start.** Cannot recommend new items (no co-occurrence data)
  or recommend for new users (no history).
- **Sparsity.** Most users interact with few items; similarity scores
  are noisy.
- **Popularity bias.** Popular items dominate; long-tail items rarely
  recommended.
- **Computation.** Naive user-user is `O(U²)`. Naive item-item is
  `O(I²)`. Modern CF uses ANN indexing or matrix factorization to
  scale.
- **No content awareness.** Two items that share genre but never
  co-occur look unrelated.

### Modern variants

- **kNN-CF.** User-based or item-based with explicit neighborhood
  size (k-nearest items or users).
- **Slope One, Slim, EASE.** Linear methods that learn item-item
  weights; surprisingly strong baselines.
- **Matrix factorization.** Factor `R` into user and item embeddings;
  see [04-matrix-factorization.md](04-matrix-factorization.md).
- **Neural collaborative filtering.** Replace the inner product with a
  neural network. Often less accurate than matrix factorization for
  the cost.
- **Two-tower retrieval.** Generalizes CF with rich features and a
  scalable ANN backend.

## Why It Matters in Real Jobs

Three production reasons. First, **strong baseline**. Item-based CF
with cosine similarity often gets within 5-10 percent of a deep model
at much lower cost; useful as a baseline against which to validate
deep models. Second, **interpretability**. Stakeholders understand
"customers who bought this also bought this" in ways they do not
understand a deep model. Third, **cold-start fallback**. When the
deep ranker fails (new user, new context), CF heuristics often save
the day.

In 2026, pure CF rarely runs as the primary ranker, but lives on as
a candidate generator, a fallback, and a sanity check.

## How It Works Step by Step

1. **Build the user-item matrix.** Sparse format (CSR or COO).
2. **Choose user-based or item-based.** Item-based for production
   (item similarities are more stable).
3. **Compute similarities.** Cosine of item columns. For very large
   catalogs, use ANN indexing (HNSW on item embeddings derived from
   the matrix).
4. **Pick neighborhood size K.** Typical 20-100. Smaller K is
   faster; larger K is more robust.
5. **Score candidate items.** Weighted sum over neighborhood.
6. **Filter already-interacted items.** Do not recommend items the
   user already bought.
7. **Apply diversity and freshness rules.** Pure CF tends to repeat
   patterns.
8. **Evaluate.** Recall@K, NDCG@K offline; CTR, retention online.

## Real-World Example

A retail company has 5M users and 200K products, 50M interactions
in the last 90 days. They build item-based CF: cosine similarity
between item columns of the interaction matrix, top-100 most-
similar items per item precomputed nightly.

For each user, they retrieve top-100 candidates by summing item-item
similarities to the user's last 30 days of items. This gives 100
candidates per user, served at 10 ms p99 from a precomputed lookup
table.

Offline NDCG@10 is 0.31. They then build a two-tower deep retrieval
model; offline NDCG@10 is 0.39 (a 25 percent relative improvement).
Online A/B test: deep retrieval lifts CTR by 7 percent and watch
time by 4 percent. They ship deep retrieval as the primary candidate
source. CF stays in the system as a backup and as one of three
candidate sources fed into the ranker (the others being deep
retrieval and recently-popular items). The CF candidates contribute
about 15 percent of the final clicks.

## Common Mistakes

- Treating zero entries in implicit feedback as "did not like";
  often they mean "did not see".
- Using user-based CF with millions of users; item-based is much
  more scalable.
- Forgetting to filter items the user already interacted with.
- Computing cosine on raw counts where popular items dominate; weight
  by inverse item frequency or normalize by item magnitude.
- Setting neighborhood size K based on intuition without
  cross-validation.
- Ignoring cold start; CF cannot recommend new items.
- Using offline metrics (NDCG@10) as the deployment criterion; A/B
  test always.
- Skipping diversity reranking; CF tends to recommend more of the
  same.

## Interview Angle

**Question:** Compare user-based and item-based collaborative
filtering, and explain why item-based dominated production for many
years.

**Strong answer:** Both methods score (user, item) pairs by
similarity over the user-item interaction matrix. The difference is
which dimension you compute similarities on.

**User-based.** For target user `u`, find the K most similar users
(by cosine of their interaction vectors), then recommend items those
K users liked that `u` has not seen. Score: weighted sum of neighbors'
interactions, weighted by similarity.

**Item-based.** Compute item-item similarities (cosine of the item
columns). For target user `u`, score each candidate item `i` by the
similarity to items `u` has already interacted with: weighted sum of
sim(i, j) over u's past items j.

Why item-based dominated production.

1. **Stability.** Item characteristics change slowly (a movie does
   not transform). User behavior changes constantly (new sessions,
   new interests, mood). Item-item similarities are stable; user-user
   similarities drift fast.

2. **Computability.** With `U` users and `I` items, the user-user
   similarity matrix is `U x U`; the item-item matrix is `I x I`.
   For most products, `I << U` (a few hundred thousand items, tens of
   millions of users). The item matrix is much smaller and easier to
   precompute and update.

3. **Caching.** The top-K most similar items for each item can be
   precomputed and cached. Serving is a lookup, microseconds. User-
   based requires recomputing neighborhoods as user vectors change.

4. **Interpretability.** "People who bought this also bought" is a
   natural product framing that maps directly to item-based CF.

The downsides of CF in general.

- Cold start. New items have no co-occurrence data; CF cannot
  recommend them.
- Sparsity. Most users have few interactions; similarities are
  noisy.
- Popularity bias. Popular items dominate; the long tail is
  underexposed.

In 2026, item-based CF is rarely the primary recommender; matrix
factorization, two-tower deep retrieval, and learned-to-rank models
have replaced it for production rankers. But it lives on as a
candidate generator, a fallback for cold start in the user dimension,
and a strong baseline against which to validate deeper models.

**Weak answer:** "User-based and item-based are similar" without
explaining why item-based scaled better.

**Follow-up questions:**

- How would you handle implicit feedback in CF?
- What is the difference between Jaccard and cosine similarity?
- Why does CF struggle with cold start?
- How does matrix factorization improve over kNN-CF?

## Mini Exercise

Take the MovieLens 100K dataset. Build item-based CF with cosine
similarity and neighborhood size K=50. Compute NDCG@10 on a held-out
set. Compare to a popularity-only baseline.

## Diagram

```mermaid
flowchart LR
    U[User u] --> H[u's past items]
    H --> S[For each candidate item i: weighted sim to past items]
    Sim[Precomputed item-item similarities] --> S
    S --> R[Rank candidates by score]
    R --> F[Filter already-interacted items]
    F --> Top[Top-K recommendations]
```

---
## Navigation

[⬅ Previous](01-recommender-systems-overview.md) | [🏠 Home](../README.md) | [➡ Next](03-content-based-filtering.md)
