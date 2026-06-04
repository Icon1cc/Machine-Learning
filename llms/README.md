# LLMs

## Folder Purpose

Transformer decoder architecture, pretraining, instruction tuning, prompting, tools, evaluation, and serving.

## Beginner Intuition

A large language model is a next-token predictor trained on huge text corpora, then aligned to follow
instructions. It is probabilistic, so it can sound confident and be wrong. The engineering skill is
not "use a bigger model"; it is wrapping the model in a clear task contract, the right context
strategy, an evaluation loop, and production controls.

## Why It Matters

LLMs power chat assistants, copilots, search, and agents. They also fail in expensive ways:
hallucination, stale knowledge, prompt injection, runaway cost, and latency. Knowing when to prompt,
retrieve, fine-tune, or add tools, and how to measure each, is the core of modern AI engineering.

## Who Should Read This Section

Read this if you build LLM applications or interview for AI/LLM-engineer roles. It pairs directly with
the RAG, agents, vector-database, and production-AI sections.

## Recommended Reading Order

Read in order: what an LLM is, tokenization, decoder architecture, pretraining, instruction tuning and
RLHF, context windows, prompting, tools, evaluation, hallucinations, guardrails, fine-tuning vs RAG,
small models, serving, then system design and interview patterns.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is An LLM](01-what-is-an-llm.md) |
| 2 | [Tokenization For LLMs](02-tokenization-for-llms.md) |
| 3 | [Transformer Decoder Architecture](03-transformer-decoder-architecture.md) |
| 4 | [Pretraining](04-pretraining.md) |
| 5 | [Instruction Tuning](05-instruction-tuning.md) |
| 6 | [RLHF And Preference Optimization](06-rlhf-and-preference-optimization.md) |
| 7 | [Context Windows](07-context-windows.md) |
| 8 | [Prompt Engineering](08-prompt-engineering.md) |
| 9 | [Function Calling Tool Use](09-function-calling-tool-use.md) |
| 10 | [LLM Evaluation](10-llm-evaluation.md) |
| 11 | [Hallucinations](11-hallucinations.md) |
| 12 | [Guardrails](12-guardrails.md) |
| 13 | [Fine Tuning Vs RAG](13-fine-tuning-vs-rag.md) |
| 14 | [Small Language Models](14-small-language-models.md) |
| 15 | [LLM Serving And Inference](15-llm-serving-and-inference.md) |
| 16 | [LLM System Design](16-llm-system-design.md) |
| 17 | [LLM Interview Patterns](17-llm-interview-patterns.md) |

## Real-World Examples

- A support assistant that drafts replies from retrieved policy with citations and abstention.
- A coding copilot using function calling to run and read code.
- A document Q&A tool that must say "not found" instead of guessing.
- A routing layer sending easy queries to a small model and hard ones to a large one.

## Pattern Recognition

- "Answers are confidently wrong" points to missing retrieval or a weak generation contract.
- "Knowledge is stale" points to RAG, not fine-tuning.
- "Need stable format or style" points to fine-tuning or few-shot prompting.
- "Latency and cost too high" points to streaming, caching, routing, and context trimming.

## Common Mistakes

- Using a bigger model as the default fix.
- Fine-tuning to memorize facts that change.
- Adding retrieval without measuring retrieval recall.
- Trusting LLM-as-judge scores without calibration or human checks.

## Interview Notes

Expect "prompt vs RAG vs fine-tune", "how do you reduce hallucination", "how do you evaluate an LLM
feature", "what is the context window cost". Strong answers pick the narrowest intervention that fixes
a measured failure.

## What You Should Know After Finishing

- How an LLM is pretrained and then aligned to follow instructions.
- When to prompt, retrieve, fine-tune, or add tools.
- How to evaluate quality with hard examples and rubrics.
- How serving choices (caching, KV cache, routing) control cost and latency.

## Suggested Exercises

- For one LLM feature, write the task contract, baseline, metric, and a refusal rule.
- Decide prompt vs RAG vs fine-tune for three different problems and justify each.
- Design an LLM-as-judge and explain how you would calibrate it.
- List three latency or cost levers for a slow chat assistant.

## Navigation

[🏠 Home](../README.md)
