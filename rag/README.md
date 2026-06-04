# RAG

## Folder Purpose

Document ingestion, chunking, embeddings, retrieval, reranking, generation, evaluation, observability, and security.

## Beginner Intuition

Retrieval-augmented generation grounds an LLM's answer in documents you fetch at query time, instead
of trusting the model's memory. The key mental model: debug retrieval and generation separately. If
the right passage was never retrieved, no prompt can fix the answer. If it was retrieved but the
answer is still wrong, the generation contract is weak.

## Why It Matters

RAG is the default way to make LLMs answer over private, large, or changing knowledge without
retraining. It is everywhere in enterprise AI, and it is a top interview topic because it forces you
to reason about chunking, hybrid search, reranking, citations, permissions, and prompt injection.

## Who Should Read This Section

Read this if you build knowledge assistants, search, or document Q&A, or interview for AI-engineer
roles. It builds on the vector-database, NLP, and LLM sections.

## Recommended Reading Order

Read in order: what RAG is, RAG vs fine-tuning, ingestion, chunking, embeddings, retrieval, hybrid
search and reranking, query rewriting, context compression, generation, evaluation, observability,
security, advanced patterns, then system design and interview patterns.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is RAG](01-what-is-rag.md) |
| 2 | [RAG Vs Fine Tuning](02-rag-vs-fine-tuning.md) |
| 3 | [Document Ingestion](03-document-ingestion.md) |
| 4 | [Chunking Strategies](04-chunking-strategies.md) |
| 5 | [Embedding Models](05-embedding-models.md) |
| 6 | [Retrieval Strategies](06-retrieval-strategies.md) |
| 7 | [Hybrid Search And Reranking](07-hybrid-search-and-reranking.md) |
| 8 | [Query Rewriting](08-query-rewriting.md) |
| 9 | [Context Compression](09-context-compression.md) |
| 10 | [Answer Generation](10-answer-generation.md) |
| 11 | [RAG Evaluation](11-rag-evaluation.md) |
| 12 | [RAG Observability](12-rag-observability.md) |
| 13 | [RAG Security](13-rag-security.md) |
| 14 | [Advanced RAG Patterns](14-advanced-rag-patterns.md) |
| 15 | [Production RAG System Design](15-production-rag-system-design.md) |
| 16 | [RAG Interview Patterns](16-rag-interview-patterns.md) |

## Real-World Examples

- An internal policy assistant that answers from HR and legal docs with citations and permissions.
- Customer support grounded in a product knowledge base, abstaining when evidence is missing.
- Developer docs Q&A that links every claim back to a source page.
- A research assistant that retrieves, reranks, and compresses context before answering.

## Pattern Recognition

- "Answer is wrong but the doc exists" points to a retrieval miss (chunking, search, reranking).
- "Right passage retrieved, wrong answer" points to the generation contract or context order.
- "Leaks restricted content" points to filtering after retrieval instead of before ranking.
- "A document told the model to ignore instructions" points to prompt injection defenses.

## Common Mistakes

- Starting with embeddings before defining the corpus and permissions.
- Skipping a BM25 or keyword baseline.
- Increasing top-k without measuring context precision or token cost.
- Measuring only final answer quality, never retrieval recall.

## Interview Notes

Expect "design a RAG system", "how do you evaluate RAG", "how do you handle permissions and prompt
injection", "chunking strategy". Strong answers separate retrieval and generation metrics and treat
retrieved text as data, not instructions.

## What You Should Know After Finishing

- The five RAG stages: ingest, chunk, retrieve, generate, evaluate.
- How hybrid search and reranking improve retrieval.
- A cite-or-abstain generation contract and why it matters.
- How to evaluate retrieval (recall@k, context precision) and answers (faithfulness, citations).

## Suggested Exercises

- Design RAG for one corpus: metadata fields, chunking rule, retrieval baseline, answer contract.
- Write a retrieval metric and an answer metric and explain why both are needed.
- Walk through how you would stop a prompt-injection attack from a poisoned document.
- Decide RAG vs fine-tuning for a fast-changing knowledge base and justify it.

## Navigation

[🏠 Home](../README.md)
