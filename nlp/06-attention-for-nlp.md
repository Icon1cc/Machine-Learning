# Attention for NLP

## Beginner-Friendly Intuition

Before attention, the sequence-to-sequence pipeline went: encoder reads
the entire input and squeezes it into a single fixed-length vector;
decoder generates the output one token at a time, conditioned only on
that vector. The bottleneck was obvious: a single vector cannot carry
enough information about a 50-word sentence, let alone a 500-word
document. Translation accuracy degraded sharply for long sequences.

Attention (Bahdanau et al., 2014; Luong et al., 2015) broke that
bottleneck. Instead of compressing the encoder output into one vector,
it kept all the encoder hidden states, and at each decoder step, the
decoder learned to **attend** to the most relevant encoder positions
for the current output. The decoder's effective "context" became a
weighted sum of all encoder states, with weights computed dynamically.

This was the architectural innovation that, scaled up and applied to
self-attention rather than only encoder-decoder attention, became the
transformer. Attention turned sequence modeling from a recurrence-bound
problem into a parallel-friendly one and enabled every modern NLP
breakthrough since.

## Formal Explanation

### The encoder-decoder bottleneck

Pre-attention seq2seq:

```
encoder: x_1, ..., x_T  ->  (h_1, ..., h_T)  ->  h_T as context
decoder: at each step t, generate y_t given y_{<t} and h_T
```

The decoder sees only the final encoder hidden state. For a 30-word
French translation of a 50-word English sentence, the decoder must
extract all 50 words of meaning from a single 512-dim vector. As input
length grows, BLEU drops.

### Attention solves the bottleneck

Attention-augmented seq2seq:

```
encoder: produces (h_1, ..., h_T) as context vectors
decoder: at step t, compute context c_t = Σ_i α_{ti} h_i,
         where weights α_{ti} are computed by an attention mechanism
         conditioned on the decoder's current state
generate y_t given y_{<t} and c_t
```

Now the decoder sees a different, dynamically-weighted version of the
encoder for each output token. Long inputs no longer require lossy
compression.

### Bahdanau attention (additive)

Compute attention scores with a small feedforward network:

```
score(s_{t-1}, h_i) = v^T tanh(W_s s_{t-1} + W_h h_i)
α_{ti} = softmax(score(s_{t-1}, h_i)) over i
c_t = Σ_i α_{ti} h_i
```

`s_{t-1}` is the decoder's hidden state. The attention weights are
positive and sum to 1.

### Luong attention (multiplicative)

Replace the feedforward score with a dot product:

```
score(s_t, h_i) = s_t · h_i        (dot)
              or s_t · W h_i        (general)
              or v^T tanh(W [s_t; h_i])  (concat)
```

Faster than additive; a strict ablation showed minor accuracy
differences on translation. Multiplicative attention is what the
transformer's scaled dot-product attention generalizes.

### Self-attention

Bahdanau and Luong attention only connect the decoder to the encoder
(cross-attention). Self-attention applies the same idea within a single
sequence: every token attends to every other token in the same input.
This is the core operation of transformers, covered in
[../deep-learning/11-attention-mechanism.md](../deep-learning/11-attention-mechanism.md).

### Visualizing attention

Attention weights `α_{ti}` form an alignment matrix between input and
output tokens. For translation, this matrix often shows interpretable
alignments: French verb "mange" attends strongly to English verb
"eats", subject "il" to "he", object "pomme" to "apple".

This was the first time NLP models produced interpretable internal
state. The attention matrix gave us a window into what the model was
"looking at." For modern transformers with many heads and many layers,
the picture is murkier; specific heads often pick up specific patterns
(syntactic dependencies, coreference, positional structure), but no
clean global story emerges.

### What attention is and is not

- **Is.** A learned, soft, weighted lookup over a memory of vectors.
  The keys index, the queries probe, the values are returned weighted.
- **Is not.** A causal explanation. Attention weights tell you what
  the model focused on; they do not tell you why it produced its
  output. Two heads can attend to similar things but the value
  projections do different work.

### Cost

Attention has cost `O(T_q · T_k · d)` where `T_q, T_k` are query and
key sequence lengths and `d` is the model dimension. For self-attention
with `T_q = T_k = T`, this is `O(T² · d)`, the famous quadratic cost.
For cross-attention in an encoder-decoder model, `T_q` is the decoder
length and `T_k` is the encoder length; long encoders are still costly
but the asymmetry helps.

## Why It Matters in Real Jobs

Attention-augmented sequence models were the production state-of-the-art
for translation from roughly 2015 to 2017. The transformer made them
obsolete by 2018, but the conceptual core (soft weighted lookup over a
memory) remains the foundation of every sequence model. Understanding
attention is necessary to understand transformers, retrieval systems
that use cross-attention rerankers, and any modern NLP architecture
diagram.

In 2026, you rarely implement Bahdanau or Luong attention directly. You
use a transformer that contains both self-attention and cross-attention
as components. But the interview question "what problem did attention
solve in seq2seq?" is still asked, and the answer (the fixed-length
bottleneck) is still the right one.

## How It Works Step by Step

1. **Recognize the bottleneck.** A model that compresses a long
   sequence into a single vector before decoding is bottlenecked by
   that vector's capacity.
2. **Replace single-vector context with attention.** At each decoder
   step, compute a weighted sum of all encoder hidden states, with
   weights determined by the decoder's current state.
3. **Pick the score function.** Dot-product is fastest; additive
   (Bahdanau) is slightly more expressive at the cost of an extra
   matmul.
4. **Add masking when needed.** Causal mask for decoder self-attention,
   padding mask for variable-length batches.
5. **Inspect attention weights.** They are interpretable for simple
   models; for deep transformers, look for specific patterns rather
   than expecting a clean global story.
6. **Use multi-head attention.** Multiple attention computations in
   parallel, with different projections, give the model the capacity to
   attend to different relations simultaneously.

## Real-World Example

A team trains a small encoder-decoder translation model in 2017 (well
before transformers were the default). Without attention, BLEU on a
test set is 22.4. After adding Luong attention, BLEU jumps to 27.8.
Inspecting the attention weights for sample translations shows that the
model has learned word alignments without explicit supervision: the
French "manger" (to eat) consistently attends to English "eat",
"eats", or "ate" depending on the conjugation. The attention
visualization becomes a debugging tool: when a translation is wrong, the
team checks where the model attended and often spots that the attention
went to the wrong English word.

## Common Mistakes

- Computing attention over the wrong axis (e.g., across batch instead
  of across sequence positions); silently produces wrong outputs.
- Forgetting padding masks; padding tokens get attention weight and
  their values are mixed into the context.
- Treating attention as a causal explanation rather than a statistical
  weight.
- Using single-head attention where multi-head would help; capacity is
  wasted.
- Applying attention only at the final decoder layer; modern designs
  apply it at every layer.
- Logging average attention weights across heads and layers and
  drawing conclusions; specific heads do specific things, averaging
  destroys the signal.
- Ignoring the `O(T²)` cost when scaling up; long-context attention
  needs FlashAttention or alternative architectures.

## Interview Angle

**Question:** What problem did attention solve in encoder-decoder
sequence models, and why was it such a big deal?

**Strong answer:** Pre-attention seq2seq compressed the entire encoder
output into a single fixed-length context vector and conditioned the
decoder on it. For a 30-word translation of a 50-word source sentence,
all 50 words of meaning had to fit into one 512-dim vector. As source
sentences got longer, the decoder lost information, and BLEU dropped
sharply for inputs above 20-30 tokens.

Attention removed the bottleneck by keeping all encoder hidden states
and letting the decoder produce, for each output token, a different
weighted combination of them. The weights were computed dynamically
from the decoder's current state and the encoder states (the score
function). Implementations vary (additive in Bahdanau, multiplicative
in Luong), but the structure is the same: a learned soft lookup over
the encoder memory.

Why it was a big deal. First, **direct accuracy gains**: 5-10 BLEU
points on long-input translation, with the same encoder/decoder
capacity. Second, **interpretability**: the attention matrix between
source and target tokens often showed meaningful alignments, the first
time we could "see" what a neural sequence model was doing. Third, and
most consequentially, attention was the conceptual seed of the
transformer. Vaswani et al. (2017) generalized attention from "decoder
attends to encoder" to "every token attends to every other token in
the same sequence" (self-attention) and removed recurrence entirely.
Self-attention is parallelizable, has `O(1)` path length between any
two positions, and scales gracefully. The transformer enabled BERT,
GPT, and the entire modern NLP stack.

So the lineage is: encoder-decoder bottleneck -> Bahdanau/Luong
attention -> self-attention -> transformer -> pretrained language
models -> LLMs. The bottleneck observation in 2014 was the start of
the chain that produced GPT-4 in 2023.

**Weak answer:** "Attention helps the model focus" without naming the
bottleneck or the lineage to transformers.

**Follow-up questions:**

- What is the difference between additive and multiplicative attention?
- How does self-attention differ from encoder-decoder attention?
- Why is it important to scale by `sqrt(d_k)` in scaled dot-product
  attention?
- Are attention weights causal explanations of model output?

## Mini Exercise

Implement Luong attention in NumPy: given a query vector and a list of
key/value vectors, compute the dot-product scores, softmax, and the
weighted sum. Compare to PyTorch's
`F.scaled_dot_product_attention` on the same inputs.

## Diagram

```mermaid
flowchart LR
    EH[Encoder hidden states h_1...h_T] --> SC[Score(s_t, h_i) for each i]
    DS[Decoder state s_t] --> SC
    SC --> SM[Softmax over i]
    SM --> CT[Context c_t = Σ α_ti h_i]
    CT --> DG[Decoder generates y_t]
```

---
## Navigation

[⬅ Previous](05-sequence-modeling.md) | [🏠 Home](../README.md) | [➡ Next](07-transformers-for-nlp.md)
