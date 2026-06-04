# NLP

## Folder Purpose

Text preprocessing, tokenization, embeddings, sequence modeling, transformers, semantic search, and NLP evaluation.

## Beginner Intuition

NLP turns text into numbers a model can use, then maps those numbers to a task: classify, tag,
extract, retrieve, or generate. The field moved from counting words, to learned word vectors, to
contextual transformer representations, and each step captured more meaning.

## Why It Matters

Most "LLM" products are NLP pipelines underneath: clean text, tokenize, embed, retrieve, classify, or
generate, then evaluate. Knowing the classical ladder lets you ship a cheap strong baseline before
reaching for an expensive model.

## Who Should Read This Section

Read this if you build text features, search, classification, or anything that becomes an LLM
application. It connects the deep-learning section to the LLM, RAG, and vector-database sections.

## Recommended Reading Order

Read in order: overview, preprocessing, tokenization, embeddings, sequence modeling, attention,
transformers, then the task lessons (classification, NER, semantic search) and evaluation.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [NLP Overview](01-nlp-overview.md) |
| 2 | [Text Preprocessing](02-text-preprocessing.md) |
| 3 | [Tokenization](03-tokenization.md) |
| 4 | [Word Embeddings Word2vec Glove Fasttext](04-word-embeddings-word2vec-glove-fasttext.md) |
| 5 | [Sequence Modeling](05-sequence-modeling.md) |
| 6 | [Attention For NLP](06-attention-for-nlp.md) |
| 7 | [Transformers For NLP](07-transformers-for-nlp.md) |
| 8 | [Text Classification](08-text-classification.md) |
| 9 | [Named Entity Recognition](09-named-entity-recognition.md) |
| 10 | [Semantic Search](10-semantic-search.md) |
| 11 | [NLP Evaluation](11-nlp-evaluation.md) |

## Real-World Examples

- Support-ticket routing with TF-IDF plus logistic regression as a fast, explainable baseline.
- Named-entity recognition pulling names, dates, and amounts from contracts.
- Semantic search over a help center using sentence embeddings and a vector index.
- Summarization and translation with encoder-decoder or decoder-only models.

## Pattern Recognition

- "Classify short texts fast" points to TF-IDF plus a linear model first.
- "Find similar meaning, not exact words" points to embeddings and vector search.
- "Rare words break my vocabulary" points to subword tokenization (BPE, WordPiece).
- "The word means different things in context" points to contextual (transformer) embeddings.

## Common Mistakes

- Reaching for a large model when TF-IDF answers the question.
- Ignoring tokenization, which affects cost and rare-word handling.
- Judging generation only by BLEU or ROUGE with no human check.
- Using accuracy on imbalanced text classes instead of macro-F1.

## Interview Notes

Expect "TF-IDF vs embeddings", "why subword tokenization", "static vs contextual embeddings", "how
would you build text classification". Show that you start cheap and upgrade only with measured gain.

## What You Should Know After Finishing

- The representation ladder from bag-of-words to contextual embeddings.
- Why subword tokenization solves out-of-vocabulary words.
- How to pick a baseline and metric for a text task.
- Which metric fits classification, retrieval, and generation.

## Suggested Exercises

- Build a TF-IDF plus logistic-regression classifier on a small text set and report macro-F1.
- Explain why "bank" needs contextual embeddings to disambiguate.
- Design semantic search for a FAQ: embedding model, index, and metric.
- Choose evaluation metrics for a summarizer and justify them.

## Navigation

[🏠 Home](../README.md)
