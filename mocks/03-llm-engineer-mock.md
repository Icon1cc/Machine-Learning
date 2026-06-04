# LLM Engineer Mock

## Scenario

You are interviewing for an LLM Engineer role. The prompt: "Our production support chat assistant has
two complaints from users and the business. First, it sometimes states confident answers that are
wrong. Second, p95 latency is 9 seconds and costs are climbing. Diagnose and fix both without
degrading answer quality."

## Round Format

A 60-minute round: 5 minutes clarifying the current system, 15 minutes diagnosing hallucination, 20
minutes on the latency and cost path, 10 minutes on evaluation, and 10 minutes on a safe rollout.

## Interviewer Prompt

This is a debugging and optimization problem on a live LLM system. Separate the two issues, propose
targeted fixes for each, and prove the fixes work without hand-waving.

## Expected Clarification Questions

- Is the assistant already using retrieval, or answering from the model's parametric memory?
- What model and context size are we on now, and where does the 9 seconds go?
- Do we have logs of wrong answers, and are they wrong because of missing or misused evidence?
- What is the quality bar and who reviews regressions?
- Are answers streamed to the user or returned all at once?

## Expected Answer or Design

A strong candidate refuses to treat "hallucination" and "latency" as one problem. For correctness,
first determine whether the right evidence is even retrieved. If retrieval misses, fix chunking,
hybrid search, and reranking before touching the prompt. If evidence is present but ignored,
constrain the generation contract: answer only from retrieved context, cite sources, and abstain when
evidence is missing. Fine-tuning is not the fix for factual errors on changing knowledge.

For latency and cost, profile where the 9 seconds go. Common wins: stream tokens so perceived latency
drops immediately, cache responses and the static system prompt, route easy queries to a smaller
model and reserve the large model for hard ones, shrink the context by reranking to fewer high-value
passages, and set a max-token limit. Evaluation ties it together: a hard-example set with known
answers, retrieval recall@k, answer faithfulness, plus latency and cost dashboards, all gated before
rollout with a canary.

## Worked Strong Answer Outline

1. Split the problem: correctness is mostly retrieval; latency is mostly architecture.
2. Debug retrieval first (recall@k), then constrain generation to cite-or-abstain.
3. Do not fine-tune to fix facts that change.
4. Latency: stream, cache, route to a smaller model, trim context via reranking.
5. Gate with a hard-example eval set and canary before full rollout.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Diagnosis | Separates retrieval failure from generation failure | Blames "the model" |
| Correctness fix | Cite-or-abstain, fix retrieval first | "Use a bigger or fine-tuned model" |
| Latency fix | Streaming, caching, routing, context trimming | Only "use a faster model" |
| Evaluation | Recall@k + faithfulness + latency/cost gates | "We will eyeball it" |
| Rollout | Canary and rollback | Ships to all users at once |

## Red Flags

- Proposing fine-tuning to stop factual errors on live knowledge.
- Increasing top-k or context without measuring cost or precision.
- Treating LLM-as-judge scores as ground truth with no calibration.
- No streaming despite a chat UI and 9 second latency.
- Changing the prompt and the retriever at once so cause is unknown.

## Follow-Up Questions

- Retrieval recall@5 is 0.95 but answers are still wrong. Where do you look?
- Routing to a small model dropped quality on 10 percent of queries. How do you decide the cutoff?
- How would you build the LLM-as-judge so you can trust it?

## Self-Review Checklist

- Did I separate the correctness and latency problems?
- Did I debug retrieval before changing the generator?
- Did I avoid fine-tuning as a fix for changing facts?
- Did I propose concrete latency and cost levers?
- Did I gate the change with evaluation and a canary?

---
## Navigation

[⬅ Previous](02-ml-engineer-mock.md) | [🏠 Home](../README.md) | [➡ Next](04-data-scientist-mock.md)
