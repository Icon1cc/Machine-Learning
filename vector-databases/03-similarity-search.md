# Similarity Search

## Beginner-Friendly Intuition

Similarity search asks "given this query vector, which stored vectors are
closest to it?" The answer depends on three choices: the **metric** (how
"close" is defined), the **search algorithm** (exact or approximate), and
the **filter conditions** that constrain which vectors are eligible. Get
those three right and similarity search is a one-line operation. Get one
wrong and the system silently returns the wrong neighbors.

The intuition for the metric: cosine measures direction; dot product
measures direction times magnitude; Euclidean measures geometric
distance. The right one depends entirely on how the embedding model was
trained. Use the metric the model expects; do not guess. The intuition
for the algorithm: exact search is `O(N)` per query and only practical
to a few hundred thousand vectors. Approximate search (ANN) trades a
controlled bit of recall for a 100x to 10000x speedup, and is the
production default above that scale.

## Formal Explanation

### Three metrics

For two vectors `u, v ∈ R^d`:

- **Cosine similarity.** `cos(u, v) = (u · v) / (||u|| ||v||)`. Range
  [-1, 1]; higher means more similar. Ignores magnitude.
- **Dot product (inner product).** `u · v = Σ u_i v_i`. Range
  unbounded; higher means more similar. Magnitude matters.
- **Euclidean distance.** `||u - v|| = sqrt(Σ (u_i - v_i)²)`. Range
  [0, ∞); lower means more similar.

When `u` and `v` are L2-normalized to unit norm:

- `||u||² = u · u = 1`, so `||u - v||² = ||u||² - 2 u · v + ||v||² = 2
  - 2 u · v`. Therefore minimizing Euclidean distance is equivalent to
  maximizing dot product, which equals cosine similarity.
- **Cosine = dot product = monotone-equivalent to Euclidean** on
  normalized vectors.

This is why production systems with sentence-transformer or
similar embeddings normalize at write time and serve with dot product:
the math is equivalent to cosine, but dot product is faster on every
ANN index implementation.

### Choosing the metric

Decide by the embedding model's training objective.

- **Trained with cosine loss** (most sentence-transformers, BGE, E5,
  most retrieval-tuned models). Use cosine, or equivalently dot
  product on normalized vectors. Normalize at write time.
- **Trained with raw dot-product loss** (some two-tower recommenders
  where magnitude encodes popularity or confidence). Use dot product
  on the raw vectors. Do not normalize.
- **Trained with Euclidean / L2 loss** (some image-similarity models,
  classical sift descriptors). Use Euclidean.

Mismatch between training and serving metric is one of the most common
silent retrieval bugs. Score curves still look reasonable; recall on
known-good queries collapses by 5-15 points.

### kNN: exact search

Brute-force: compute the metric between the query and every stored
vector, sort, return top-K. Cost: `O(N · d)` per query. Implementations:
NumPy with batched matmul, FAISS-flat, scikit-learn `BallTree`, or any
DB's exact-search mode.

Practical limit: about 100K to 1M vectors at 1024 dim on a single CPU
core for sub-100 ms latency. Above that, you need ANN.

Exact search is essential as a **recall ground truth** for ANN
evaluation; even at 100M vectors, you can compute exact search on a
1000-query sample to measure ANN recall.

### ANN: approximate nearest neighbor

ANN trades recall for speed. The standard quality-cost levers:

- **Recall@K.** Of the true top-K nearest neighbors (by exact search),
  what fraction does ANN return? Typical production target: 0.95-0.99.
- **Latency.** Per-query time, often p50 and p99.
- **Memory.** Bytes per vector, including index overhead.
- **Build time.** How long it takes to construct or update the index.

The main ANN families: **HNSW** (graph-based, low latency, high memory),
**IVF + product quantization** (cluster-based, lower memory), **DiskANN**
(SSD-based for huge corpora). Covered in
[`04-indexing-hnsw-ivf-pq.md`](04-indexing-hnsw-ivf-pq.md).

Each ANN method has a tunable that trades recall for latency:

- HNSW: `efSearch` (higher = more candidates explored = higher recall,
  higher latency).
- IVF: `nprobe` (number of clusters to search).
- DiskANN: similar exploration parameter.

Sweep this parameter to draw a recall-vs-latency curve and pick the
operating point that meets your SLA.

### Recall measurement

A vector index's behavior is invisible without measurement. Standard
practice:

1. Build an exact-search index on a sample of 10K to 1M vectors.
2. Sample 500 to 5000 query vectors representative of production.
3. Compute exact top-K for each query.
4. Compute ANN top-K with current settings.
5. Recall@K = mean over queries of `|exact ∩ ann| / K`.

Production teams run this monthly; recall can drift as the corpus
evolves, the index is rebuilt, or parameters are retuned.

### Filtered nearest neighbor

Adding a metadata filter (`category = 'shoes' AND price < 50`) to the
ANN search has two semantics:

- **Pre-filter.** Restrict the candidate set first, then ANN over the
  restricted set. Recall is preserved relative to the filter; latency
  depends on filter selectivity.
- **Post-filter.** ANN-search top-K, then drop results that fail the
  filter. Cheaper but recall collapses if the filter is selective
  (many top-K results get dropped, leaving few or none).

Most production systems prefer pre-filter when filter selectivity is
moderate; post-filter when the filter is rarely true. See
[`05-metadata-filtering.md`](05-metadata-filtering.md).

## Why It Matters in Real Jobs

Three production reasons. First, **wrong metric, wrong recall**. The
single largest silent quality bug in vector search is using a metric
the embedding model was not trained for. Second, **ANN tuning is the
quality-cost knob**. The same index can serve at recall 0.85 in 3 ms or
recall 0.99 in 30 ms; picking the right operating point is real
engineering. Third, **filtered search interactions** are subtle and
domain-specific; the same query at the same recall can fail or succeed
depending on the filter strategy.

## How It Works Step by Step

1. **Pick the metric** based on the embedding model's training. When
   in doubt, normalize and use dot product.
2. **Build an exact-search baseline** on a sample. This is the recall
   ground truth.
3. **Build the ANN index** with default parameters.
4. **Measure recall@K** on a query set against exact. Tune the
   exploration parameter (efSearch, nprobe) to hit the recall target.
5. **Measure latency p50 and p99** at the chosen recall.
6. **Decide on filter strategy** for each common filter type
   (pre-filter for selective, post-filter for rare).
7. **Document the operating point**: index parameters, recall target,
   latency budget, filter strategy.
8. **Re-run the recall measurement periodically.** Drift is silent.

## Real-World Example

A team has 8M product description embeddings (1024 dim, BGE-M3
normalized). Their first deployment: HNSW with `m = 16, ef_construction
= 200, ef_search = 64`. Memory: ~35 GB. Latency p50: 2 ms; p99: 8 ms.
Recall@10 against exact search: 0.91. They ship.

Three weeks later, customer complaints rise: "the search misses items I
know are similar." Investigation: at recall 0.91, 9 percent of true
top-10 are missed per query, which is visible to power users. They
sweep `ef_search` from 64 to 256. At `ef_search = 192`: recall@10 0.97,
p99 latency 18 ms, well within the 50 ms budget. They redeploy.

A month later, they realize Euclidean was being computed (FAISS
default) instead of dot product on their normalized vectors. Equivalent
on math but the index was tuned for Euclidean comparisons. Switching
the metric flag costs 0.5 ms latency and restores 1 percent recall.
The lesson: defaults are not your friend.

## Common Mistakes

- Mismatching the metric: cosine-trained model served with Euclidean.
  Quality drops silently.
- Not normalizing when the embedding model expects unit-norm. Cosine
  and dot product give different results.
- Skipping the recall measurement. Without exact-search ground truth,
  ANN quality is invisible.
- Using a single recall number to characterize the index. Recall
  varies with K, with the query distribution, and with corpus drift.
- Tuning recall without tuning latency. They are dual; you need a
  curve, not a point.
- Treating filter as free. A pre-filter on a selective predicate can
  10x your latency.
- Confusing similarity with relevance. Closest in embedding space is
  not the same as most useful to the user; reranking and business
  rules close the gap.
- Forgetting that ANN parameters affect both build time and query
  time. A higher-recall index takes longer to build.

## Interview Angle

**Question:** You inherit a semantic-search system with poor relevance.
The embedding model and corpus seem fine. Where do you investigate the
similarity-search layer?

**Strong answer:** Three things, in order of likelihood.

First, **metric mismatch.** What metric is the model trained for, and
what metric is the index using? If the model is cosine-trained
(typical for sentence-transformers and BGE-family) and the index is
configured for Euclidean (FAISS default), or if the model expects
unit-norm vectors and they are not being normalized at write time,
recall collapses by 5-15 points without any error signal. The fix is
a one-line config change.

Second, **ANN recall.** Is the index returning the actual top-K, or
some approximation? Build an exact-search index on a 100K sample,
measure recall@K of the production ANN against it on a representative
query set. If recall is below 0.9, the ANN parameters need tuning
(`ef_search` higher, `nprobe` higher, more probes for IVF, deeper
graph for HNSW). The latency-recall curve gives you a principled
operating point.

Third, **filter strategy.** If queries include metadata filters, is
the system pre-filtering or post-filtering? With a selective filter,
post-filter can return zero or near-zero results; with a non-
selective filter, pre-filter can blow latency. The production answer
is usually a hybrid: pre-filter for high-selectivity filters,
post-filter for rare ones, with a fallback path.

Beyond these three, the relevance gap might be in the embedding model
itself (does its training data resemble production?), in the chunking
(too long or too short hurts retrieval), or in the ranking layer
(reranker, recency, or business rules). But for the similarity-search
layer specifically, the three above account for most production bugs
I have seen.

**Weak answer:** "Try a bigger model." That trades months of
re-embedding for an unmeasured gain.

**Follow-up questions:**

- Why does dot product equal cosine on normalized vectors?
- How do you measure recall@K without computing exact search on the
  whole corpus?
- What is the difference between pre-filter and post-filter in ANN?
- When would you pick Euclidean over cosine?

## Mini Exercise

Take any small embedding dataset. Compute exact top-10 for 100
queries. Then build an HNSW index with low `ef_search` and a high
`ef_search`. Plot recall@10 against latency. Pick an operating point
that hits recall 0.95 and measure the latency.

## Diagram

```mermaid
flowchart LR
    Q[Query vector] --> M{Search type}
    M -- Exact --> KNN[Brute-force kNN: O(N·d)]
    M -- Approx --> ANN[ANN index: HNSW / IVF / DiskANN]
    KNN --> R[Top-K + scores]
    ANN --> R
    R --> Eval[Recall@K vs exact baseline]
```

---
## Navigation

[⬅ Previous](02-embeddings.md) | [🏠 Home](../README.md) | [➡ Next](04-indexing-hnsw-ivf-pq.md)
