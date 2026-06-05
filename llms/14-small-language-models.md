# Small Language Models

## Beginner-Friendly Intuition

Bigger is not always better. Small language models (a few billion parameters or fewer) are cheaper, faster,
and can run on modest hardware or even on-device. For many narrow, well-defined tasks they match or beat a
giant model at a fraction of the cost and latency. The skill is knowing when a small model is enough, often
after fine-tuning it on the specific task.

## Formal Explanation

Small language models trade raw general capability for efficiency: lower inference cost, lower latency,
smaller memory footprint, and the option to run locally for privacy. They tend to underperform large models
on open-ended reasoning and broad knowledge, but a small model fine-tuned on a narrow task (classification,
extraction, routing, a fixed format) can be competitive or superior for that task. Techniques like
distillation (training a small model to mimic a large one) and quantization (reducing weight precision)
further shrink cost. The pattern is often: prototype with a large model, then distill or fine-tune a small
one for production.

## Why It Matters in Real Jobs

Cost and latency at scale are real constraints. Serving a giant model for every request, including trivial
ones, is wasteful. Routing easy or narrow tasks to a small model (or running one on-device for privacy) can
cut cost dramatically while keeping quality. On-device small models also enable offline and privacy-sensitive
use cases. Understanding this lets you design systems that are economical, not just capable.

## How It Works Step by Step

1. **Prototype** with a large model to establish the quality bar.
2. **Identify narrow tasks** suitable for a smaller model.
3. **Fine-tune or distill** a small model on those tasks.
4. **Optionally quantize** to shrink memory and speed up inference.
5. **Route** easy or narrow requests to the small model, hard ones to the large one.

**Diagnosing task narrowness.** A task is narrow enough for a small model when: the input space is
bounded (intent classification with K classes, structured extraction from a known schema, FAQ over a
fixed corpus), the output is short or structured (a label, a JSON object, a 1-2 sentence response),
and the reasoning depth is limited (no multi-step chain-of-thought, no external knowledge synthesis).
General open-ended chat fails all three criteria; small models stumble there. A 3B-parameter model
(Llama-3.2-3B, Phi-3-mini, Qwen-2.5-3B) typically reaches large-model-quality on narrow tasks after
fine-tuning on 1K-10K examples.

**Distillation cost.** Three steps: (1) run the teacher (large model) over a labeled dataset to
produce target outputs or token-level logits, (2) train the student (small model) on those targets,
(3) validate. Teacher inference cost dominates: distilling on 100K examples through a frontier-tier
hosted model can cost hundreds to thousands of dollars in API fees. Self-hosted teacher cuts this
substantially; expect a few GPU-days. Student training is comparatively cheap (few hours on a single
GPU). Validate that the student matches the teacher on a held-out set before deploying.

**Routing-model latency.** When a router decides which model to use per request, the router itself
must be fast: a small classifier (DistilBERT-class, 5-15 ms on CPU) or an embedding-based nearest-neighbor
lookup (1-5 ms). Add the router latency to both routes' total budget. A common pattern: router decides;
small model handles 70-90 percent of traffic; complex requests escalate to the large model. Track the
escalation rate; if it climbs, the router or the small model needs work.

## Real-World Example

A product runs every chat through a large model and the bill is unsustainable. Analysis shows 70 percent of
requests are simple intent classification and FAQ lookups. The team fine-tunes a small model for those,
routes them away from the large model, and reserves the large model for complex open-ended queries. Cost
drops sharply with no quality loss on the easy traffic. A privacy-sensitive on-device feature uses a
quantized small model so data never leaves the device.

## Common Mistakes

- Defaulting to the largest model for every task regardless of cost.
- Expecting a small model to match a large one on open-ended reasoning.
- Skipping fine-tuning, then concluding the small model "is not good enough".
- Ignoring quantization and distillation as cost levers.

## Interview Angle

**Question:** When would you use a small language model?

**Strong answer:** For narrow, well-defined tasks at scale, or on-device for privacy. I prototype with a
large model, then fine-tune or distill a small one for production and route easy traffic to it, reserving the
large model for hard queries. Quantization cuts cost further.

**Weak answer:** "Always use the biggest model for best quality."

**Follow-up questions:**

- What is distillation?
- What does quantization trade off?
- How would you decide the routing cutoff?

## Mini Exercise

For a product with mixed-difficulty requests, propose which tasks go to a small model and which to a large
one, and name one technique (distillation or quantization) you would apply and why.

## Diagram

```mermaid
flowchart TD
    A[Request] --> B{Task difficulty}
    B -- Narrow / easy --> C[Small fine-tuned model]
    B -- Complex / open-ended --> D[Large model]
    C --> E[Lower cost + latency]
    D --> F[Higher capability]
    C -. shrink .-> G[Distillation / quantization]
```

---
## Navigation

[⬅ Previous](13-fine-tuning-vs-rag.md) | [🏠 Home](../README.md) | [➡ Next](15-llm-serving-and-inference.md)
