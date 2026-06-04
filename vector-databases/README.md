# Vector Databases

## Folder Purpose

Embeddings, similarity search, ANN indexes, filtering, hybrid search, reranking, and vector search scaling.

## Beginner Intuition

A vector database stores embeddings and finds the nearest ones to a query fast. Exact nearest-neighbor
search is too slow at scale, so these systems use approximate nearest neighbor (ANN) indexes that
trade a little recall for a large speedup. The whole job is "given this vector, return the closest k,
quickly, with filters".

## Why It Matters

Vector databases are the retrieval engine under RAG, semantic search, recommendations, and
deduplication. The index choice is a real engineering tradeoff between recall, latency, memory, and
build time, and getting it wrong shows up as slow search, blown memory budgets, or missed results.

## Who Should Read This Section

Read this if you build search or RAG, or interview for AI-engineer roles that probe ANN indexes and
hybrid retrieval. It sits directly under the RAG section and connects to NLP embeddings.

## Recommended Reading Order

Read in order: what a vector database is, embeddings, similarity search, ANN indexes (HNSW, IVF, PQ),
metadata filtering, hybrid search, reranking, database selection, scaling, then interview patterns.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is A Vector Database](01-what-is-a-vector-database.md) |
| 2 | [Embeddings](02-embeddings.md) |
| 3 | [Similarity Search](03-similarity-search.md) |
| 4 | [Indexing HNSW IVF PQ](04-indexing-hnsw-ivf-pq.md) |
| 5 | [Metadata Filtering](05-metadata-filtering.md) |
| 6 | [Hybrid Search](06-hybrid-search.md) |
| 7 | [Reranking](07-reranking.md) |
| 8 | [Vector Db Selection](08-vector-db-selection.md) |
| 9 | [Scaling Vector Search](09-scaling-vector-search.md) |
| 10 | [Vector Database Interview Patterns](10-vector-database-interview-patterns.md) |

## Real-World Examples

- RAG retrieval over millions of document chunks with metadata filters for permissions.
- Semantic product search where "running shoes" matches "trainers".
- Near-duplicate detection across a large content library.
- Recommendation candidate generation from item embeddings.

## Pattern Recognition

- "Need fast high-recall search on moderate scale" points to HNSW.
- "Billions of vectors, memory constrained" points to IVF-PQ.
- "Only return docs this user can see" points to native metadata filtering before ranking.
- "Search results are mediocre" points to adding hybrid search and a reranker.

## Common Mistakes

- Using a distance metric that does not match the embedding model.
- Assuming ANN returns exact neighbors (it does not).
- Ignoring HNSW memory cost at large scale.
- No plan for updates, deletes, or re-embedding when the model changes.

## Interview Notes

Expect "how does ANN work", "HNSW vs IVF", "what metric for text embeddings", "how do you filter by
metadata and handle updates". Show that you reason about the recall-latency-memory triangle and would
measure recall@k.

## What You Should Know After Finishing

- How ANN indexes trade recall for speed.
- HNSW vs IVF vs PQ and when each fits.
- How metadata filtering and hybrid search improve results.
- How to scale and keep an index fresh.

## Suggested Exercises

- For 200M vectors and a 50 ms budget, pick an index, a metric, and the knob you would tune.
- Explain why ANN recall must be measured, not assumed.
- Design metadata filtering for a permission-aware search.
- Describe how you would handle deletes and re-embedding.

## Navigation

[🏠 Home](../README.md)
