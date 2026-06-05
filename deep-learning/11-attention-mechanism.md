# Attention Mechanism

## Beginner-Friendly Intuition

Attention lets a model look at all positions in a sequence at once and
decide, for each output position, how much to weigh each input position.
Instead of squeezing all the input information through a single fixed-size
hidden state (the bottleneck in RNN encoder-decoder models), attention
gives the decoder direct, weighted access to the entire encoder output.

The intuition: imagine translating an English sentence to French. To
produce each French word, you do not need to remember the entire English
sentence equally. You need to focus on the few English words that
correspond to the French word you are about to write. Attention is the
mechanism that learns those focus weights.

Attention transformed sequence modeling. The 2017 transformer paper
removed recurrence and convolution entirely and built a model out of
nothing but attention plus feedforward layers. That architecture, scaled
up, produced BERT, GPT, ViT, and every large language model since.

## Formal Explanation

The basic operation is **scaled dot-product attention**. Given queries
`Q ∈ R^{T_q × d_k}`, keys `K ∈ R^{T_k × d_k}`, and values
`V ∈ R^{T_k × d_v}`:

```
Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
```

Each query computes a similarity (dot product) with every key. The
similarities are scaled by `sqrt(d_k)` and softmaxed into a distribution
over the keys. The output for each query is a weighted sum of the values,
weighted by these attention scores. So each query "looks up" relevant
information across all key-value pairs.

### Why scale by `sqrt(d_k)`

Without scaling, the dot products `Q K^T` have variance growing with
`d_k`. For `d_k = 64`, the standard deviation of a dot product is around
8, which produces softmax outputs near one-hot (saturated). The gradient
through a saturated softmax is near zero, so training stalls. Dividing by
`sqrt(d_k)` keeps the variance constant and softmax in a well-behaved
range.

### Self-attention

When `Q`, `K`, and `V` all come from the same sequence (typically by
linearly projecting the same input), it is **self-attention**. Each
position attends to every other position (including itself) in the same
sequence. This is what transformers use as their core operation.

Self-attention's input shape is `(B, T, d)` where `d` is the model
dimension. Three linear projections produce `Q, K, V` each of the same
shape. The output is `(B, T, d)`.

Computational cost is `O(T² · d)`: dominated by the `Q K^T` matmul of
shape `(T, d_k) × (d_k, T)`. This **quadratic cost in sequence length**
is why long context is expensive in transformers and why FlashAttention
and other tricks matter at scale.

### Multi-head attention

Run `h` parallel attention computations with different learned
projections, then concatenate. With `h = 8` heads and model dimension
`d = 512`, each head operates on `d_h = 64` dimensions:

```
head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)        # for i = 1..h
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
```

The intuition is that different heads can learn to focus on different
relations: one head might track grammatical agreement, another might
track coreference, another might track positional patterns. Empirically,
multi-head attention works better than a single head of equivalent total
dimension; different heads do learn distinguishable behaviors, though
analyzing them is hard.

### Cross-attention

When `Q` comes from one sequence and `K, V` from another, it is
**cross-attention**. Used in encoder-decoder architectures: the decoder's
queries attend to the encoder's keys and values. Every decoder layer has
both self-attention (over the decoder's own outputs so far) and
cross-attention (over the encoder's output).

### Masking

In autoregressive (decoder-only) models, each position can only attend to
positions before it (causal mask). Implementation: set the upper-triangular
entries of the attention score matrix to `-∞` before softmax, which makes
the softmax weights zero for "future" positions. The model cannot cheat
by looking at the answer.

For variable-length batches with padding, a **padding mask** sets
attention scores to `-∞` for padding tokens, so they contribute nothing
to the output. Critical for correct training; missing it is a silent
accuracy bug.

### Complexity and FlashAttention

Standard attention has `O(T² · d)` compute and `O(T² + T · d)` memory.
The `T²` memory term is the score matrix; for `T = 8192`, that is 64M
floats per head. Memory is the bottleneck.

**FlashAttention** (Dao et al., 2022) computes attention without
materializing the full `T × T` score matrix. It tiles the computation,
uses an online softmax pass, and recomputes intermediate values during
the backward pass. Same math, much smaller memory traffic, dramatically
faster wall-clock at long context. It is the standard implementation in
2026.

Other approaches to long context: linear attention (approximate the
softmax with a kernel), sparse attention (attend only to a structured
subset), state space models (S4, Mamba) that recover linear-time
sequence modeling.

## Why It Matters in Real Jobs

Attention is the operational core of every modern sequence model. Every
LLM, every vision transformer, every speech model with a transformer
backbone, every retrieval system using cross-encoders, runs attention
internally. Three production reasons. First, **understanding cost
profiles**: the `T²` complexity is what determines context-length pricing
in API products and inference latency in edge deployments. Second,
**debugging**: attention weights are interpretable. You can visualize
what positions a head attends to and diagnose why a model makes a
specific decision. Third, **architecture design**: choosing between
self-attention, cross-attention, mask patterns, and number of heads is a
core design skill for any sequence model.

## How It Works Step by Step

1. **Project inputs to Q, K, V.** Three linear layers, one per role.
2. **Reshape for multi-head.** `(B, T, d) -> (B, h, T, d_h)`.
3. **Compute attention scores.** `Q K^T / sqrt(d_h)`.
4. **Apply mask if needed.** Causal mask for decoders, padding mask for
   variable-length inputs.
5. **Softmax over the key dimension.** Produces attention weights.
6. **Multiply by V.** Weighted sum of values.
7. **Concatenate heads and project.** Final linear layer to mix heads.
8. **Add residual and normalize.** Standard transformer block has
   pre-norm or post-norm wrapping.

## Real-World Example

A team builds a question-answering system over a 10,000-token document.
With standard attention and a 2-layer model, GPU memory tops out at 4096
tokens. They switch to FlashAttention; same model, same accuracy, now
fits 16,384 tokens in the same memory at 1.6x faster wall-clock. They
also enable causal masking only on the answer-generation portion of the
sequence, allowing bidirectional attention on the document. Per-query
latency drops from 380 ms to 220 ms. The architecture math (attention)
did not change; the memory layout (FlashAttention) and mask design did
all the work.

## Common Mistakes

- Forgetting the `sqrt(d_k)` scaling; softmax saturates and training
  stalls.
- Forgetting the padding mask in variable-length batches; padding tokens
  contribute to the output.
- Forgetting the causal mask in autoregressive training; the model cheats
  and validation accuracy looks great until inference.
- Computing `Q K^T` and storing it for backprop on long sequences;
  memory blows up. Use FlashAttention.
- Setting too many heads (16-32) on a small model dimension (`d = 256`);
  per-head dim becomes very small and capacity is wasted.
- Mixing up the order of softmax and the mask; mask must be applied
  before softmax, not after.
- Using attention without a residual connection; deeper transformers
  become hard to train.
- Treating attention weights as causal explanations; they are model
  internals, not ground truth about input importance.

## Interview Angle

**Question:** Walk through scaled dot-product attention, including why
each component is there.

**Strong answer:** Given queries `Q`, keys `K`, values `V`, compute
`softmax(Q K^T / sqrt(d_k)) V`.

The query-key dot product `Q K^T` measures similarity: row `i` column
`j` is the alignment between query `i` and key `j`. The motivation is
that we want each output position to "look at" relevant positions, and
dot products are the natural similarity measure for embeddings.

The scaling by `sqrt(d_k)` exists because the dot product of two random
`d_k`-dim vectors with i.i.d. unit-variance entries has variance `d_k`.
For `d_k = 64`, the standard deviation is 8. Softmax of a vector with
standard deviation 8 produces near-one-hot outputs and the gradient
through the softmax is near zero. Dividing by `sqrt(d_k)` brings the
variance back to 1, keeping softmax in a region with useful gradient.
The exact `sqrt(d_k)` (rather than `d_k`) comes from
`Var(x / c) = Var(x) / c²`, so dividing by `sqrt(d_k)` reduces variance
back to 1.

The softmax converts scores into a probability distribution over keys.
Each output is then a weighted sum of values. The "soft" attention
(softmax weights, not hard one-hot) is what makes attention
differentiable; gradients flow through the weights to the queries and
keys.

Multi-head attention runs this `h` times in parallel with different
projections, lets different heads learn different relations, and
concatenates the results. The total parameter count and compute are
roughly the same as single-head with full dimension, but capacity is
better used.

Self-attention applies this with `Q, K, V` all from the same input
sequence. Cross-attention has `Q` from one sequence and `K, V` from
another. Causal masking prevents attending to future positions in
autoregressive models.

The cost is `O(T² · d)` per head, dominated by the `Q K^T` matmul. This
is why long-context models need FlashAttention or linear-time
alternatives.

**Weak answer:** Reciting the formula without justifying the scaling or
explaining what each operation accomplishes.

**Follow-up questions:**

- Why divide by `sqrt(d_k)` specifically?
- What is multi-head attention and why use it?
- What is the memory cost of attention and what is FlashAttention?
- How do causal and padding masks work?

## Mini Exercise

Implement scaled dot-product attention in NumPy. Test on small random
tensors. Then add multi-head support by reshaping. Compare your
implementation to PyTorch's `F.scaled_dot_product_attention` on the same
inputs.

## Diagram

```mermaid
flowchart LR
    Q[Query Q] --> S[Q K^T / sqrt(d_k)]
    K[Key K] --> S
    S --> M[Apply mask]
    M --> SM[Softmax over keys]
    SM --> O[Weighted sum: scores · V]
    V[Value V] --> O
    O --> Out[Output]
```

---
## Navigation

[⬅ Previous](10-rnns-lstms-grus.md) | [🏠 Home](../README.md) | [➡ Next](12-transformers.md)
