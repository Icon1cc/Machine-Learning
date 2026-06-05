# Batch Normalization and Layer Normalization

## Beginner-Friendly Intuition

Batch normalization and layer normalization rescale activations during
training so they stay in a well-behaved range. Without normalization, deep
networks suffer from a cascade of changing activation scales: layer 1's
output distribution shifts during training, layer 2's input distribution
shifts as a result, layer 3's input shifts even more, and so on. By the
time you reach layer 30, gradients vanish or explode and training stalls.

Normalization fixes this by forcing the activations at each layer to have
a fixed scale (standardized to mean 0, variance 1) plus a learned
per-feature scale and shift. The network gets the freedom to learn the
right scale for each feature, but the cascade of drift is broken. The net
effect is that you can train deeper networks, with higher learning rates,
and they converge faster.

The two main flavors differ in **what they normalize over**: batch norm
normalizes across the batch dimension, layer norm normalizes across the
feature dimension. The choice depends on the architecture and the data.

## Formal Explanation

For a tensor of activations `x` (shape depends on layer type), the basic
operation is:

```
μ = mean(x over normalization axes)
σ² = var(x over normalization axes)
x̂ = (x - μ) / sqrt(σ² + ε)
y = γ x̂ + β
```

where `γ` (scale) and `β` (shift) are learned per-feature parameters and
`ε` is a small constant for numerical stability. The normalization
**reduces the dependence between layers** during training and enables
faster convergence.

### Batch Normalization (BN)

Normalize across the batch dimension. For an activation of shape
`(B, C)` (an MLP layer):

- Compute mean and variance across the batch (the `B` dimension), per
  feature (`C`).
- Normalize. Apply learned `γ` and `β` per feature.

For a CNN activation of shape `(B, C, H, W)`:

- Mean and variance across `(B, H, W)`, per channel `C`.
- Each channel is treated as one "feature."

**Train vs eval mode** is critical for BN:

- During training, use the current mini-batch's statistics. Maintain a
  running average of mean and variance (typical decay 0.99) for inference.
- During inference, use the running statistics. Forgetting to call
  `model.eval()` uses batch statistics in inference, which is wrong if the
  inference batch is small or single-example.

BN's strengths:

- Speeds up training of deep CNNs by 5-10x in some classical settings.
- Allows higher learning rates without divergence.
- Mild regularization effect; train/test gap often narrows.
- The original 2015 paper (Ioffe and Szegedy) framed this as solving
  "internal covariate shift." More recent work (Santurkar et al., 2018)
  argues the real benefit is **smoothing the loss landscape** rather than
  fixing covariate shift; the gradient becomes less sensitive to changes in
  earlier layers.

BN's weaknesses:

- **Small batch sizes break it.** With batch size 1, BN reduces to
  identity (no statistics to compute). Below batch size 16-32, BN
  statistics are too noisy and training degrades. A common production
  problem: a model trained with batch 256 deployed with batch 1 produces
  different outputs.
- **Distributed training requires synchronization.** Cross-GPU batches
  must share statistics, or each GPU computes its own (less accurate).
  SyncBN handles this at communication cost.
- **Train-vs-eval distribution mismatch.** Production data may have
  different statistics than training; the running averages may be wrong.

### Layer Normalization (LN)

Normalize across the feature dimension. For an activation of shape
`(B, T, d)` (a transformer):

- Compute mean and variance across `d`, per token (`B, T`).
- Normalize. Apply learned `γ` and `β` per feature.

LN does not depend on batch size, so it works with any batch (including
batch size 1) and does not maintain running statistics. **Train and eval
are identical** for LN. This is why transformers use LN almost
universally.

### When to use which

- **CNNs (image classification, detection, segmentation).** Batch norm
  is standard. Use SyncBN for distributed training.
- **Transformers and sequence models.** Layer norm. Always.
- **RNNs.** Layer norm. BN does not handle the recurrent statistics
  cleanly.
- **Reinforcement learning.** Layer norm or no normalization. BN's
  running statistics interact badly with non-stationary RL targets.
- **Very small batches.** Layer norm or group norm.

### Variants

- **GroupNorm (Wu and He, 2018).** Splits channels into groups and
  normalizes each group. Independent of batch size. Used when small
  batches are unavoidable in CNNs.
- **InstanceNorm.** Normalizes each example's channel independently. Used
  in style transfer.
- **RMSNorm (Zhang and Sennrich, 2019).** A simplified LayerNorm without
  the mean subtraction (only divides by RMS). Used in LLaMA and many
  recent transformer variants. Slightly faster, similar accuracy.

### Pre-norm vs post-norm

In a transformer, normalization can go before or after the residual:

- **Post-norm** (original transformer): `y = LayerNorm(x + Attention(x))`.
  Harder to train at depth.
- **Pre-norm** (modern transformers): `y = x + Attention(LayerNorm(x))`.
  Easier to train, default in GPT, LLaMA, ViT.

Pre-norm became standard because it allows much deeper models to train
without warmup tuning gymnastics.

## Why It Matters in Real Jobs

Three production reasons. First, **training large models requires
normalization**. Models above ~10 layers without it are nearly impossible
to train. Second, **inference correctness depends on it**. The eval-mode
behavior is part of the model's contract; getting it wrong silently
returns wrong outputs. Third, **deployment constraints determine the
choice**. If you have to serve at batch size 1, BN is wrong; switch to LN
or GroupNorm.

The interview question is rarely "what is batch norm?" but "why do
transformers use layer norm?" or "what happens if you serve a BN model at
batch size 1?". The depth of your answer signals how many models you have
actually shipped.

## How It Works Step by Step

1. **Pick the normalization by architecture.** BN for CNNs, LN for
   transformers, GroupNorm for small-batch CNNs.
2. **Place it correctly.** In a CNN: conv -> BN -> activation. In a
   transformer pre-norm block: residual = x + Attention(LN(x)). Order
   matters; BN before activation is more common than after.
3. **Initialize gamma and beta sensibly.** `γ = 1`, `β = 0` is the standard.
   Some recipes initialize `γ = 0` for the last BN/LN of a residual block
   to ease training (residual init).
4. **Set train/eval mode correctly.** `model.train()` for training,
   `model.eval()` for validation and inference.
5. **For distributed training with BN, use SyncBN.** Single-GPU BN with
   small per-GPU batch produces noisy statistics.
6. **Watch for inference-time issues.** Production batch size 1 with BN
   uses running statistics; verify the running statistics are not stale or
   biased toward training distribution.

## Real-World Example

A team trains a ViT (vision transformer). They use post-norm initially;
training is unstable above 12 layers. They switch to pre-norm; the model
trains cleanly to 24 layers. They deploy with batch size 1 (each user
uploads a single image). LN means train-time and inference-time behavior
are identical; no statistics to track. Compare to a parallel project with
a CNN classifier. They use BatchNorm during training with batch 256.
Inference at batch 1 must use running statistics, and a memory bug in
deployment caused stale running stats; predictions drifted by 8 percent
in production until they noticed. Both projects ship; the LN-based one
has fewer deployment gotchas.

## Common Mistakes

- Forgetting `model.eval()` before inference; BN uses batch statistics
  instead of running statistics, producing wrong outputs at small batch.
- Using BN in a transformer; transformers benefit from LN, not BN.
- Using BN with batch size 1 or 2; statistics are too noisy to be
  meaningful.
- Forgetting to handle the running-statistics divergence between training
  and serving; production data may be very different.
- Placing normalization in the wrong order (BN after activation when
  before is conventional, or layer norm after residual sum when pre-norm
  is required).
- Not using SyncBN in multi-GPU training; per-GPU statistics differ from
  the cross-GPU statistics, hurting accuracy.
- Setting the BN momentum too high (rarely updated running stats) or too
  low (too noisy).
- Treating LN's learned `γ` and `β` as redundant; they matter for some
  layers and removing them hurts.

## Interview Angle

**Question:** Why do transformers use layer normalization instead of batch
normalization, and what changes if you swap them?

**Strong answer:** Three reasons.

First, **batch independence**. LN normalizes across the feature dimension
of each token independently. The batch dimension is irrelevant. BN
normalizes across the batch dimension, which makes its statistics depend
on what other examples happen to be in the batch. Transformers are often
trained with sequence packing or variable-length inputs; the effective
"batch" the BN sees has highly variable structure, while LN does not care.

Second, **train-eval consistency**. LN computes statistics from the
current input. There is no running average to maintain; inference and
training behave identically. BN must store running mean and variance and
switch to them at inference. This is more code, more state to manage, and
a known source of inference bugs (forgetting `model.eval()`, stale
statistics, train-vs-prod batch size mismatch). For transformers served at
batch size 1 (interactive use), BN's running statistics need to be very
accurate to match training-time behavior.

Third, **sequence-level effects**. In a transformer, each token attends to
many other tokens. Normalizing across the batch dimension would mix
statistics across unrelated sequences, which is conceptually wrong. LN
normalizes within each token, which respects the sequence structure.

If you swap BN in for LN in a transformer, the immediate symptoms are:
training instability, especially at the start when running statistics are
warming up; sensitivity to batch size (small batches degrade); and worse
inference at batch size 1. Some research has tried (BatchNorm++ in
"PowerNorm") and shows that with careful work BN can be made competitive,
but standard BN is clearly worse in transformers, which is why layer norm
became the universal choice.

**Weak answer:** "Transformers use LN because that's what BERT did" without
reasoning about batch dependence or train/eval.

**Follow-up questions:**

- What is the difference between pre-norm and post-norm?
- What is GroupNorm and when do you use it?
- Why does BN fail at batch size 1?
- What is RMSNorm and how does it differ from LayerNorm?

## Mini Exercise

Train a small transformer with LayerNorm and with BatchNorm. Compare
training stability and final validation accuracy. Note where BN training
diverges (often early epochs).

## Diagram

```mermaid
flowchart LR
    X[Activation x] --> M[Mean and variance over normalization axes]
    M --> N[Normalize: x̂ = (x - μ) / sqrt(σ² + ε)]
    N --> A[Affine: y = γ x̂ + β]
    A --> Out[Output]
    BN[BN: axes = batch] --> M
    LN[LN: axes = features] --> M
    GN[GroupNorm: axes = feature groups] --> M
```

---
## Navigation

[⬅ Previous](07-regularization-dropout-weight-decay.md) | [🏠 Home](../README.md) | [➡ Next](09-cnns.md)
