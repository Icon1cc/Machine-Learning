# Instruction Tuning

## Beginner-Friendly Intuition

A base model completes text but does not reliably do what you ask. Instruction tuning teaches it to follow
instructions by training it on many examples of (instruction, good response) pairs. After this, "Summarize
this email" produces a summary instead of more email. It is the step that turns a raw text predictor into a
helpful assistant.

## Formal Explanation

Instruction tuning is supervised fine-tuning (SFT) on a curated dataset of instruction-response pairs across
many tasks (summarize, translate, answer, classify, reason). The model keeps its pretrained knowledge but
shifts its behavior toward following directions and producing the desired format. Quality and diversity of
the instruction data matter more than raw quantity; a smaller, cleaner set of well-written examples often
beats a larger noisy one. SFT typically precedes preference optimization (RLHF or DPO), which further refines
helpfulness and safety.

In practice, **SFT data saturates surprisingly fast**. The LIMA paper (Zhou et al., 2023) showed that
1,000 carefully-curated instruction-response pairs were enough to align a strong base model on
general-purpose chat. Production teams typically work in the **1K-10K range for narrow tasks** (a specific
output format or domain) and **10K-100K for general assistant behavior**. Beyond that, returns diminish
sharply on a fixed compute budget. The bigger risk is **catastrophic forgetting**: aggressive SFT on a
narrow task can degrade general reasoning. Mitigations include using a low learning rate (1e-5 to 1e-6 for
full SFT, 1e-4 for LoRA), training for fewer epochs (1-3 typical), mixing in a small fraction of
diverse general data ("rehearsal"), and preferring **LoRA or QLoRA** over full fine-tuning when the
adapter weights can be loaded only when needed. The cleanest framing for the SFT vs RAG decision: SFT
shifts **distribution of behavior** (format, tone, narrow skill); it does not reliably teach **new facts**.
Facts that change should live in retrieval; behavior that should be consistent can live in the SFT mix.

## Why It Matters in Real Jobs

Instruction tuning is why you can prompt a model in plain language and get useful behavior. For teams, a
light domain instruction-tune can lock in a response format, tone, or task pattern that prompting alone
struggles to make reliable. But it does not add live knowledge (that is retrieval's job), and over-tuning on
narrow data can degrade general ability. Knowing what instruction tuning does and does not fix prevents
misusing it.

## How It Works Step by Step

1. **Curate** diverse, high-quality instruction-response pairs.
2. **Fine-tune** the base model on them with supervised learning.
3. **Validate** that instruction-following improved without losing general ability.
4. **Follow with preference optimization** to refine helpfulness and safety.
5. **Deploy** the aligned model, adding retrieval for facts.

## Real-World Example

A team needs every model response in a strict clause-by-clause legal format. Prompting gets it right most of
the time but occasionally drifts. A light instruction-tune on a few hundred well-formatted examples makes the
format reliable. They deliberately keep facts out of the tuning data (those change) and supply them via
retrieval instead, so knowledge stays fresh while behavior stays consistent.

## Common Mistakes

- Expecting instruction tuning to add factual knowledge (it does not).
- Using a large noisy dataset instead of a smaller high-quality one.
- Over-tuning on narrow data, hurting general capability.
- Conflating instruction tuning (behavior) with retrieval (knowledge).

## Interview Angle

**Question:** What does instruction tuning do, and what does it not do?

**Strong answer:** It teaches a base model to follow instructions via supervised fine-tuning on
instruction-response pairs, improving behavior and format. It does not add live knowledge; that needs
retrieval. Data quality matters more than quantity.

**Weak answer:** "It trains the model on our data to know our domain," conflating behavior and knowledge.

**Follow-up questions:**

- Why does data quality beat quantity here?
- How does instruction tuning relate to RLHF?
- What problems should you not solve with instruction tuning?

## Mini Exercise

Give one problem instruction tuning would fix (a behavior or format) and one it would not (a fact). Explain
the right approach for each.

## Diagram

```mermaid
flowchart LR
    A[Base model] --> B[Instruction-response pairs]
    B --> C[Supervised fine-tuning]
    C --> D[Follows instructions + format]
    D --> E[Preference optimization]
    E --> F[Aligned assistant]
    F -. facts via .-> G[Retrieval, not tuning]
```

---
## Navigation

[⬅ Previous](04-pretraining.md) | [🏠 Home](../README.md) | [➡ Next](06-rlhf-and-preference-optimization.md)
