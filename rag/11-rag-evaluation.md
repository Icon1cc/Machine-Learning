# RAG Evaluation

## Beginner-Friendly Intuition

You cannot improve a RAG system you cannot measure, and "the answers look good" is not measurement. The
key insight is to evaluate retrieval and generation separately, because a bad answer can come from either.
If retrieval missed the evidence, fix retrieval; if the evidence was present but the answer was wrong or
uncited, fix generation. Two dials, two sets of metrics.

## Formal Explanation

RAG evaluation has two layers. Retrieval metrics: recall@k (did the relevant chunk appear in the top k),
context precision (how much of the retrieved context is relevant), and MRR. Generation metrics:
faithfulness (does every claim follow from the retrieved context), answer relevance (does it address the
question), and citation accuracy (do citations support their claims). You need a labeled evaluation set:
questions paired with the gold passages and ideally gold answers. LLM-as-judge can scale faithfulness
scoring but must be calibrated against human labels.

**RAGAS** (Es et al., 2023) is the standard metric framework in 2026. The four core metrics:

- **Faithfulness.** For each claim in the answer, is it supported by the retrieved context? Computed
  by extracting claims from the answer and checking each against the context with an LLM-as-judge
  configured for entailment. Score range 0-1; production targets above 0.9.
- **Answer relevance.** Does the answer address the user's question? Computed by generating
  questions from the answer and measuring similarity to the original. Catches off-topic responses.
- **Context precision.** Of the retrieved passages, how many are relevant? Catches noise.
- **Context recall.** Of the gold-relevant content, how much made it into the retrieved context?
  Catches retrieval misses.

The four metrics together identify which stage failed. Low context recall means retrieval; high
context recall plus low faithfulness means generation; high faithfulness plus low answer relevance
means the model misread the question. Open-source implementation: `ragas` library; integrates with
LangSmith, LangFuse, and other RAG observability stacks.

**Eval set size guidance.** 50-100 questions for early iteration and quick comparisons; 200-500 for
serious launch decisions; 1000+ for detecting <2 percent quality differences in production. Bootstrap
confidence intervals on each metric tell you if your eval set distinguishes two candidates.

**Hard-example curation method.** Hand-pick or generate cases that broke the system in production
(reported by users, flagged by monitoring), tricky multi-hop questions (requiring 2+ documents),
should-abstain cases (questions the corpus does not cover), and adversarial cases (prompt injection,
out-of-scope, malformed queries). Aim for 20-50 hard cases as a regression suite; refresh quarterly
with new failure modes.

## Why It Matters in Real Jobs

Without component-level metrics, every regression is a guessing game. With them, an incident becomes
diagnosable: "recall@5 dropped after the chunking change" or "faithfulness fell after the prompt edit". A
small, well-chosen eval set plus a hard-example regression suite catches breakage before users do, which
is the entire point of evaluation-driven development.

## How It Works Step by Step

1. **Build an eval set:** questions with gold relevant passages and reference answers.
2. **Measure retrieval:** recall@k and context precision.
3. **Measure generation:** faithfulness, answer relevance, citation accuracy.
4. **Add a hard-example suite:** tricky, multi-hop, and abstain-required cases as regression tests.
5. **Automate and gate:** run on every change; calibrate any LLM judge against human labels.

## Real-World Example

A team ships a "better" embedding model and answer quality drops. Component metrics reveal recall@5 rose
but context precision fell, flooding the prompt with loosely related chunks that confused the generator.
Because they measured both layers, the fix (tighter reranking) was obvious. Had they only tracked final
answer quality, they would have blamed the model and possibly reverted the actual improvement.

## Common Mistakes

- Measuring only the final answer, so failures are unattributable.
- No labeled gold set, so metrics are vibes.
- Trusting LLM-as-judge without calibrating it against humans.
- No hard-example regression suite, so fixes silently break old cases.

## Interview Angle

**Question:** How do you evaluate a RAG system?

**Strong answer:** Separately. Retrieval with recall@k and context precision; generation with
faithfulness, answer relevance, and citation accuracy. I keep a labeled eval set and a hard-example
regression suite, and calibrate any LLM judge.

**Weak answer:** "Check if the answers are good," with no component metrics or labeled data.

**Follow-up questions:**

- How do you build a faithfulness metric?
- How do you calibrate an LLM judge?
- Why separate retrieval and generation metrics?

## Mini Exercise

Design an eval set of five questions for a corpus you know. For each, note the gold passage, and define
one retrieval metric and one generation metric you would compute, plus one hard "should abstain" case.

## Diagram

```mermaid
flowchart TD
    A[Eval set: Q + gold passages + answers] --> B[Retrieval metrics]
    A --> C[Generation metrics]
    B --> D[recall@k, context precision]
    C --> E[faithfulness, relevance, citation accuracy]
    D --> F{Regression?}
    E --> F
    F -- Yes --> G[Locate failing component]
    F -- No --> H[Gate passed]
```

---
## Navigation

[⬅ Previous](10-answer-generation.md) | [🏠 Home](../README.md) | [➡ Next](12-rag-observability.md)
