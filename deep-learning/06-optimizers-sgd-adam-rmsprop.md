# Optimizers: SGD, Adam, and RMSprop

## Beginner-Friendly Intuition

An optimizer takes the gradients computed by backpropagation and turns them
into parameter updates. The choice of optimizer decides whether your network
trains in 30 minutes or 30 hours, and whether it converges to a useful
minimum or oscillates and diverges.

The intuition: gradient descent says "move each parameter a small step in
the direction that reduces the loss." Optimizers extend this with momentum
(remember the recent direction of travel), per-parameter learning rates
(adapt to the gradient's history), and weight decay (pull weights toward
zero). The differences between SGD, RMSprop, and Adam are exactly which of
these tricks they use and how.

For 90 percent of deep learning, the answer is **AdamW**. Knowing why and
when to choose differently is what separates an engineer from a notebook
copy-paster.

## Formal Explanation

Notation: parameter `θ`, gradient `g_t = ∇L(θ_{t-1})`, learning rate `η`.

### SGD (Stochastic Gradient Descent)

```
θ_t = θ_{t-1} - η g_t
```

Plain gradient descent on a mini-batch. Sensitive to learning rate. Strong
generalization in many settings, especially CNNs trained from scratch on
ImageNet. Slow to converge on saddle-point-heavy landscapes.

### SGD with momentum

```
v_t = μ v_{t-1} + g_t
θ_t = θ_{t-1} - η v_t
```

The velocity `v_t` accumulates an exponentially weighted average of past
gradients (typical `μ = 0.9`). This helps the optimizer roll through
narrow ravines and escape shallow saddle points faster than plain SGD.
Standard for vision; often produces the best generalization in CNN
training.

### Nesterov momentum

A variant that "looks ahead" before computing the gradient:

```
g_t = ∇L(θ_{t-1} - η μ v_{t-1})
v_t = μ v_{t-1} + g_t
θ_t = θ_{t-1} - η v_t
```

Slightly faster convergence than vanilla momentum, used in some training
recipes.

### RMSprop

```
s_t = β s_{t-1} + (1 - β) g_t²       (element-wise square)
θ_t = θ_{t-1} - η g_t / (sqrt(s_t) + ε)
```

Maintains a running estimate of the squared gradient per parameter
(typical `β = 0.99`, `ε = 1e-8`). Divides the update by `sqrt(s_t)`, which
gives an adaptive per-parameter learning rate: parameters with historically
large gradients get smaller updates. Solves the "fast-direction
overshoots" problem that plain SGD has. Used heavily in RNN training and
RL.

### Adam (Adaptive Moment Estimation)

```
m_t = β_1 m_{t-1} + (1 - β_1) g_t            (first moment estimate)
s_t = β_2 s_{t-1} + (1 - β_2) g_t²            (second moment estimate)
m̂_t = m_t / (1 - β_1^t)                       (bias correction)
ŝ_t = s_t / (1 - β_2^t)                       (bias correction)
θ_t = θ_{t-1} - η m̂_t / (sqrt(ŝ_t) + ε)
```

Combines momentum (`m_t`) with RMSprop's adaptive scaling (`s_t`). Bias
corrections account for the zero-initialization of `m` and `s`. Default
hyperparameters: `β_1 = 0.9`, `β_2 = 0.999`, `ε = 1e-8`. Adam works on
almost everything with minimal tuning, which is why it became the default.

### AdamW

Standard Adam with L2 regularization adds `λ θ` to the gradient before
the optimizer's adaptive step. The adaptive scaling rescales the
regularization by `1 / sqrt(s_t)`, which means parameters with large
historical gradients get less weight decay than parameters with small
ones. That coupling is rarely what you want.

**AdamW** decouples weight decay: it applies `θ <- θ - η λ θ` as a
**separate step** after the Adam update. Decay is uniform across
parameters, independent of the gradient history. AdamW with `λ = 0.01` to
0.1 is the standard for transformers and consistently generalizes better
than Adam with the same nominal `λ` in the loss.

### Lion

A newer optimizer (Chen et al., 2023) that uses sign-of-momentum updates:

```
m_t = β_1 m_{t-1} + (1 - β_1) g_t
θ_t = θ_{t-1} - η · sign(m_t)
m_t = β_2 m_{t-1} + (1 - β_2) g_t
```

Uses less memory than Adam (only one momentum buffer instead of two) and
matches AdamW on some large-scale benchmarks. Worth knowing about; not yet
the default.

### Learning rate schedules

The learning rate is more important than the optimizer choice. Common
schedules:

- **Step decay.** Drop LR by 10x at fixed epochs. Used in classical CNN
  training.
- **Cosine annealing.** LR follows half a cosine cycle from initial to
  near-zero. Smooth and works well with warmup.
- **Linear warmup + decay.** LR ramps from 0 to peak over a warmup phase,
  then decays. Standard for transformers.
- **One-cycle.** LR ramps up, holds at peak, ramps down to a small final
  value. Good for shorter training schedules.

The combination "linear warmup over 1000-2000 steps + cosine decay to
near-zero" is the standard transformer recipe. A learning rate sweep on a
small training run is the quickest way to find a good initial value.

### Linear scaling rule

When you increase batch size by `k`, you can usually scale the learning
rate by `k` and recover similar training dynamics. Roughly accurate for `k`
up to about 8x the original batch size; beyond that, square-root scaling or
extended warmup are needed. Most papers about "training ImageNet in 1
hour" rely on this rule plus careful warmup.

## Why It Matters in Real Jobs

Three reasons. First, **default choice**: AdamW for transformers and
sequence models, SGD with momentum for CNN training from scratch. Picking
wrong costs days or weeks of training time. Second, **stability**: the
right optimizer plus warmup plus gradient clipping is what makes large
models train without diverging. Third, **the LR schedule matters more than
the optimizer once you have picked sensibly**. Most "I cannot get this
model to converge" problems are LR problems, not optimizer problems.

## How It Works Step by Step

1. **Pick the optimizer by architecture.** AdamW for transformers and
   sequence models. SGD with momentum for CNN training from scratch on
   ImageNet-style tasks. RMSprop for some RL settings.
2. **Set the initial learning rate.** Use a learning rate finder or sweep
   `lr ∈ {1e-2, 1e-3, 1e-4, 1e-5}`. For Adam, `1e-3` to `3e-4` is typical.
   For SGD, `1e-1` is typical for vision.
3. **Add warmup.** 500-2000 steps of linear ramp from 0 to peak LR. Crucial
   for transformers; helpful everywhere.
4. **Add a decay schedule.** Cosine to near zero is a strong default.
5. **Tune weight decay.** AdamW: `0.01` to `0.1` for transformers, `1e-4`
   for some vision models. SGD: typical `5e-4`.
6. **Add gradient clipping if needed.** `clip_grad_norm_(1.0)` for
   transformers and RNNs.
7. **Watch the loss curve.** Diverging means LR too high. Plateauing too
   early means LR too low or schedule wrong.

## Real-World Example

A team trains a transformer with Adam at `lr = 1e-3`. Loss explodes at
step 400. They switch to AdamW with `weight_decay = 0.01`, add 1000 steps
of linear warmup, decay to `1e-5` with cosine, and clip gradients at 1.0.
Loss is stable and reaches the target in 50 epochs. Six months later they
port the model to a 4x larger batch size; they apply the linear scaling
rule (peak LR `4e-3`, longer warmup) and training proceeds cleanly. The
optimizer choice did not change; the recipe (LR + schedule + warmup +
clipping) did all the work.

## Common Mistakes

- Using Adam with the L2 regularization in the loss instead of AdamW with
  decoupled weight decay; transformers generalize worse.
- Setting the LR too high without warmup; loss explodes in the first few
  hundred steps.
- Setting the LR too low; training plateaus at a high loss.
- Forgetting to scale the LR when changing batch size.
- Treating "optimizer" as the most important hyperparameter; the LR
  schedule matters more.
- Using SGD without momentum; convergence is much slower.
- Using a fixed LR throughout training; almost always worse than a
  schedule.
- Ignoring gradient clipping in transformers; spikes can NaN the loss.

## Interview Angle

**Question:** What is the difference between Adam and AdamW, and why does
it matter in practice?

**Strong answer:** Both use the same Adam update rule for the gradient
direction (momentum + adaptive scaling). They differ in how they apply
weight decay.

In standard Adam with L2 regularization, you add `λ θ` to the gradient
before the optimizer step:

```
g_t <- g_t + λ θ_{t-1}
... Adam update with this modified g ...
```

The Adam update divides by `sqrt(s_t)`, where `s_t` is the running second
moment. This means parameters with large historical gradients get a small
effective decay (because their `1 / sqrt(s_t)` is small), and parameters
with small historical gradients get a large effective decay. So weight
decay is gradient-dependent, which is rarely what you intended.

AdamW decouples weight decay. After computing the standard Adam update, it
applies a separate step:

```
θ_t <- (1 - η λ) θ_t  ... applied after the Adam direction update
```

Decay is uniform across parameters, independent of the second moment. The
practical effect: AdamW with `λ = 0.01` typically generalizes meaningfully
better than Adam with `λ = 0.01` in the loss. The improvement is most
visible on transformers and large models with many parameters; for very
small models the gap is small. AdamW is now the default in every modern
training recipe (BERT, GPT, ViT, modern CV).

**Weak answer:** "AdamW has weight decay" without explaining the coupling
problem.

**Follow-up questions:**

- Why is warmup important for transformers?
- What is the linear scaling rule?
- When would you choose SGD with momentum over AdamW?
- Why does Adam sometimes generalize worse than SGD?

## Mini Exercise

Train a small CNN on CIFAR-10 with three optimizers: SGD with momentum,
Adam, AdamW. Use the same learning rate (`lr = 1e-3`). Plot training and
validation accuracy over 20 epochs. Note which converges fastest and which
generalizes best.

## Diagram

```mermaid
flowchart LR
    G[Gradient g_t] --> S[SGD: θ -= η g]
    G --> M[Momentum: v = μ v + g, θ -= η v]
    G --> R[RMSprop: s = β s + (1-β) g², θ -= η g / sqrt(s)]
    G --> A[Adam: m + s + bias correction]
    A --> AW[AdamW: Adam + decoupled weight decay]
```

---
## Navigation

[⬅ Previous](05-backpropagation.md) | [🏠 Home](../README.md) | [➡ Next](07-regularization-dropout-weight-decay.md)
