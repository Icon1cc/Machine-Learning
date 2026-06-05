# Hybrid Search

## Beginner-Friendly Intuition

Hybrid search combines two scoring signals over the same corpus:
**lexical** (sparse, keyword-based, BM25) and **dense** (semantic,
embedding-based). The fusion of the two is more robust than either
alone, especially in production where queries include exact strings
(product codes, error messages, function names) **and** open-ended
natural language ("how do I cancel my account").

The intuition for why hybrid wins: dense embeddings capture semantic
similarity but often miss exact matches on rare terms. A query for
"AKB-3201" lands close to "AKZ-3402" in embedding space because they
look similar; BM25 distinguishes them perfectly. Conversely, BM25
misses paraphrases ("how do I cancel" vs "ways to terminate
membership"). The two signals are complementary; combining them
typically lifts NDCG@10 by 3-10 points over the better single signal.

In 2026, **hybrid search is the production default for serious
retrieval systems**. Pure dense retrieval is the cheaper baseline;
pure sparse is the legacy fallback; the combination is what ships.

## Formal Explanation

### BM25 (sparse baseline)

The standard term-weighting scheme for keyword search (Robertson and
Spärck Jones, 1976; Robertson 1994). For a query Q with terms t and
a document D:

```
BM25(Q, D) = Σ_t IDF(t) · (f(t, D) · (k1 + 1)) / (f(t, D) + k1 · (1 - b + b · |D| / avgdl))
```

where `f(t, D)` is term frequency in D, `|D|` is document length,
`avgdl` is average document length, `IDF(t)` is inverse document
frequency, and `k1` (typical 1.2-2.0) and `b` (typical 0.75) are
tunable hyperparameters.

Tuning matters:

- **`k1`** controls term-frequency saturation. Lower (1.0-1.2) saturates
  faster, helps on short documents and FAQ. Higher (1.5-2.0) gives
  more weight to repeated terms.
- **`b`** controls length normalization. 0.75 is the textbook default;
  lower (0.3-0.5) when document length carries meaning (legal
  contracts); 1.0 fully normalizes by length.

Default BM25 parameters work surprisingly well. Tune only when you have
an evaluation harness; otherwise leave at defaults.

Modern implementations: Elasticsearch / OpenSearch (default scorer),
Lucene, Vespa, Tantivy, Pinecone hybrid search, Qdrant sparse vectors.

### Dense retrieval

Embed query and documents with a sentence-transformer or similar
model; rank by cosine similarity (or dot product on normalized
vectors). Strong on paraphrases, semantic similarity, multilingual.

See [`02-embeddings.md`](02-embeddings.md) and
[`03-similarity-search.md`](03-similarity-search.md).

### Reciprocal Rank Fusion (RRF)

The simplest and most robust fusion method (Cormack et al., 2009).
Given multiple ranked lists, assign each item a score:

```
RRF_score(d) = Σ_lists 1 / (k + rank_in_list(d))
```

`k` is a small constant (typical 60). Items not in a list contribute
nothing. Sort by RRF score; return top-N.

Properties:

- **No score normalization needed.** Different lists can have wildly
  different score ranges; RRF only cares about ranks.
- **Robust to bad sub-rankings.** A list that returns garbage at the
  top still contributes only `1/(k+1)` for its top item.
- **Parameter-free in practice.** `k = 60` works across most domains.

Limitations:

- **Independence assumption.** RRF treats each list as independent
  evidence. If two lists agree because they share the same bias, RRF
  inflates that bias.
- **Hides poor sub-rankings.** A list whose top-K is mostly wrong is
  not penalized; you may not notice that, say, the dense path is
  silently broken.

Always monitor each sub-ranking's quality independently in addition to
RRF combined.

### Weighted score combination

Alternative to RRF: convert each list's scores to a normalized range
(min-max, z-score, or sigmoid), then combine with weights:

```
score(d) = α · sparse_score(d) + (1 - α) · dense_score(d)
```

`α` tuned on a validation set, typically between 0.3 and 0.7. The
challenge is normalization: BM25 scores are unbounded; dense cosine is
in [-1, 1] after normalization. The two need to be on comparable
scales.

Pros over RRF: more interpretable, can be tuned per query type. Cons:
fragile to score distribution shift; needs an eval set to tune `α`.

For most teams, **start with RRF**. Move to weighted combination when
you have a labeled eval set and per-query type weights matter.

### Convex combination on normalized rank

A middle ground: convert to ranks, then weight. Avoids score-scale
mismatch but does not have the score-magnitude robustness of RRF.

### When does hybrid win?

Hybrid wins consistently when queries include any of:

- **Rare terms or proper nouns.** Product codes, function names, drug
  names, place names, error messages. Dense alone misses; BM25 hits
  exactly.
- **Code or technical jargon.** Embedding models often lose code
  precision; BM25 keeps it.
- **Mixed lexical and semantic.** "How do I configure XYZ-Service for
  HTTPS" combines a specific service name and a paraphrasable concept.
- **Multilingual with code-switching.** BM25 catches the structured
  parts; dense catches the meaning.

Hybrid wins less when queries are pure paraphrase or when the corpus
has no rare-term signal (e.g., news article body text). In those
cases, dense alone is competitive.

### Hybrid search support in vector DBs

- **Pinecone.** Hybrid endpoint with sparse + dense fields.
- **Qdrant.** Sparse vector support; can score sparse and dense
  together natively.
- **Weaviate.** Hybrid query with `alpha` parameter for dense vs
  sparse mix.
- **Elasticsearch / OpenSearch.** kNN plugin alongside the BM25 native
  scorer; combine via boolean query or RRF in the query DSL.
- **pgvector.** Combine pgvector cosine with PostgreSQL `tsvector` /
  `ts_rank` BM25 in a single SQL query; fuse application-side.

The mechanics differ; the architecture pattern is the same.

### Reranking on top of hybrid

Hybrid search produces a top-K candidate list. A cross-encoder
reranker on top can further lift NDCG by 3-10 points. See
[`07-reranking.md`](07-reranking.md). Hybrid + reranking is the modern
state-of-the-art retrieval stack.

## Why It Matters in Real Jobs

Three production reasons. First, **dense retrieval alone has visible
failure modes** that hybrid fixes for free. Second, **BM25 is often
already running** in your stack (Elasticsearch, search backend); hybrid
is incremental. Third, **the lift is meaningful**: 3-10 NDCG points is
the difference between "users complain" and "users notice the search
is good."

## How It Works Step by Step

1. **Build the dense index.** Embedding model + vector index.
2. **Build the sparse index.** BM25 in Elasticsearch, OpenSearch, or
   the vector DB's sparse support.
3. **Run both at query time.** Top-100 candidates from each.
4. **Fuse with RRF.** `score = Σ 1 / (60 + rank)` across the two
   lists.
5. **(Optional)** rerank the top 50 with a cross-encoder.
6. **Return top-K.**
7. **Monitor each sub-ranking separately.** Per-list NDCG@10 plus
   combined.
8. **Tune BM25 (k1, b) and dense (ef_search) only when an eval set
   shows it is needed.**

## Real-World Example

A team builds a developer-docs search system for a SaaS product.
Queries include API names ("createInstance"), error codes ("E_AUTH_403"),
natural-language questions ("how do I rotate API keys"), and mixed
("how do I use createInstance with a service principal").

They benchmark on 200 labeled queries.

- BM25 only: NDCG@10 = 0.51. Misses paraphrases entirely.
- Dense only (BGE-M3, normalized, HNSW): NDCG@10 = 0.62. Misses exact
  API names and error codes.
- Hybrid with RRF: NDCG@10 = 0.71. Recovers the API-name and error-code
  cases.
- Hybrid + cross-encoder reranker (bge-reranker-v2-m3): NDCG@10 = 0.78.

They ship hybrid + reranker. Latency p99: dense 8 ms, BM25 12 ms,
reranker 80 ms (over top 50), total 100 ms within budget. The single
biggest jump (0.62 -> 0.71) comes from adding BM25 to dense; the
reranker provides the next biggest jump (0.71 -> 0.78). Both are worth
their cost.

## Common Mistakes

- Skipping BM25 entirely. The marginal cost is low; the lift is real.
- Using weighted score combination without normalization. Different
  score scales produce a fusion dominated by whichever has larger
  numbers.
- Treating RRF as a fix for a broken sub-ranking. RRF hides bad lists;
  monitor each independently.
- Tuning BM25 (k1, b) without an eval set. Defaults are fine until
  proven otherwise.
- Forgetting that hybrid retrieval doubles the query-time work; budget
  accordingly.
- Mixing different embedding models in the dense path of a hybrid
  system. Inconsistent semantics break the fusion.
- Reporting only combined NDCG. The combined number can mask a broken
  dense or sparse path.

## Interview Angle

**Question:** Why is hybrid search the production default for
retrieval, and how does Reciprocal Rank Fusion combine the lists?

**Strong answer:** Pure dense retrieval has well-known failure modes
that BM25 fixes for free, and pure BM25 misses paraphrases that dense
retrieval handles. The combination is more robust than either alone,
typically lifting NDCG@10 by 3-10 points over the better single
signal.

The failure modes that justify hybrid.

- **Rare terms.** Embeddings smooth over near-similar tokens; an
  exact API name like "createInstance" can land far from the relevant
  documentation in embedding space. BM25 with TF-IDF treats it as a
  rare term and ranks the right doc first.
- **Proper nouns and identifiers.** Product codes, error codes,
  function names. Dense often substitutes a near-match for the exact
  match; BM25 does not.
- **Code and structured language.** Embedding models lose precision on
  code; BM25 retains it.

For fusion, **Reciprocal Rank Fusion** is the standard. Given multiple
ranked lists, assign each item a score:

```
RRF_score(d) = Σ_lists 1 / (k + rank_in_list(d))
```

with `k = 60` typical. Items not in a list contribute 0. Sort by
score, return top-N.

Why RRF works.

- **No score normalization.** BM25 scores are unbounded; dense cosine
  is in [-1, 1]. Mixing them with weighted sum requires careful
  normalization that often breaks under distribution shift. RRF only
  uses ranks, not scores.
- **Robustness.** A list that returns garbage at top-1 contributes
  `1 / (k + 1) ≈ 1/61` to that garbage; not enough to overpower
  agreement from the other list.
- **Parameter-free in practice.** `k = 60` works across most domains
  without tuning.

Limitations of RRF.

- **Independence assumption.** Treats each list as independent
  evidence. If both lists share the same bias (e.g., both favor
  recently-indexed documents), RRF amplifies it.
- **Hides bad sub-rankings.** A list whose top-K is mostly wrong is
  not penalized in the combined score. You can only notice this by
  monitoring each list independently.

For most teams, RRF is the right default. Move to weighted score
combination only when an evaluation set shows per-query-type weighting
helps and you have the harness to detect normalization drift.

The full retrieval stack in 2026 is typically: hybrid (dense + BM25,
fused with RRF) producing ~100 candidates, then a cross-encoder
reranker on top. Each layer adds 3-10 NDCG points. Each layer also
adds latency; budget accordingly.

**Weak answer:** "Just use dense embeddings, they are better."
Misses the rare-term and identifier failure modes that hybrid
catches.

**Follow-up questions:**

- What are RRF's limitations and when would you use weighted score
  combination instead?
- How would you tune BM25 (k1, b)?
- When does pure dense retrieval beat hybrid?
- How does hybrid interact with reranking?

## Mini Exercise

Take any small corpus with mixed query types (some keyword, some
natural language). Implement BM25 and dense retrieval. Fuse with RRF
(`k = 60`). Compute NDCG@10 for each retrieval mode. Note which query
types benefit most from hybrid.

## Diagram

```mermaid
flowchart LR
    Q[Query] --> B[BM25 index]
    Q --> D[Dense vector index]
    B --> R1[Top-100 ranked]
    D --> R2[Top-100 ranked]
    R1 --> RRF[RRF fusion: Σ 1/(k + rank)]
    R2 --> RRF
    RRF --> R[Top-N candidates]
    R --> CE[Optional cross-encoder rerank]
    CE --> Out[Final top-K]
```

---
## Navigation

[⬅ Previous](05-metadata-filtering.md) | [🏠 Home](../README.md) | [➡ Next](07-reranking.md)
