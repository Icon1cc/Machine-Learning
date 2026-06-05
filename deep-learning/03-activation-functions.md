# Activation Functions

## Beginner-Friendly Intuition

An activation function is the small non-linear squish applied between layers
of a neural network. Without activations, no matter how many layers you
stack, the whole thing collapses into a single linear transformation.
Activations break that collapse and let depth do its job.

The intuition for picking one: every activation has a "well-behaved zone"
and a "saturated zone." In the well-behaved zone the gradient is decent and
the network learns. In the saturated zone the gradient is near zero and
learning stalls. Modern activations (ReLU, GELU, SiLU) keep more of their
input range in the well-behaved zone, which is the main reason deep networks
train at all today.

## Formal Explanation

### Sigmoid

`σ(z) = 1 / (1 + e^{-z})`. Output in (0, 1). Derivative `σ(z)(1 - σ(z))`,
maxes at 0.25 when `z = 0`. Saturates strongly at large `|z|`: derivative
goes to zero, gradient vanishes through stacked sigmoids. Causes the
classic "vanishing gradient" problem in deep networks. Still used as the
**output** activation for binary classification, but rarely as a hidden
activation.

### Tanh

`tanh(z) = (e^z - e^{-z}) / (e^z + e^{-z})`. Output in (-1, 1). Derivative
maxes at 1.0 when `z = 0`. Zero-centered output (unlike sigmoid), which
helps optimization. Still saturates at large `|z|`. Used in some legacy
recurrent models. Replaced by ReLU in feedforward networks.

### ReLU (Rectified Linear Unit)

`ReLU(z) = max(0, z)`. Derivative is 1 for `z > 0`, 0 for `z < 0`. The
default activation since AlexNet (2012). Reasons it dominated:

- **No saturation in the positive direction.** Gradients flow without
  decaying through depth.
- **Simple and fast.** No exponentials, just a comparison.
- **Sparse activations.** Half the units are zero on average, which is a
  mild form of regularization.

The downside is the **dead ReLU** problem: a unit can get stuck in the
negative region (where the gradient is zero) and never recover. Once dead,
the unit contributes nothing forever. Caused by large negative bias or a
single big update that pushes activations into the dead zone. Mitigations:
careful initialization (He init), lower learning rate, Leaky ReLU.

### Leaky ReLU and PReLU

`LeakyReLU(z) = max(0.01 z, z)`. Same as ReLU for positive `z`, but a small
positive slope (0.01) for negative `z`. Prevents dead units at the cost of
slightly less sparsity. PReLU learns the slope as a parameter. Used in some
vision models; ReLU is still more common.

### ELU and SELU

`ELU(z) = z` for `z > 0`, `α(e^z - 1)` for `z <= 0`. Smoother than ReLU at
zero, allows negative outputs. SELU is a self-normalizing variant that
maintains zero mean and unit variance through layers under specific
conditions. Used occasionally; rarely beats ReLU + batch norm in practice.

### GELU (Gaussian Error Linear Unit)

`GELU(z) = z · Φ(z)`, where `Φ` is the standard normal CDF. Smooth, with a
slight curvature near zero. Used in BERT, GPT, and almost every modern
transformer. The smoothness empirically helps; some recent work (Hendrycks
& Gimpel, 2016) argues the probabilistic interpretation (each unit's output
is `z` weighted by the probability that `z > 0`) provides a useful
inductive bias.

### SiLU (Swish)

`SiLU(z) = z · σ(z)`. Like GELU but using sigmoid instead of CDF.
Smooth, non-monotonic, slightly negative for small negative inputs. Used in
EfficientNet and increasingly in modern transformers (sometimes via SwiGLU,
a gated variant). Often interchangeable with GELU.

### Softmax

Applied to the final layer for multiclass classification:
`softmax(z)_i = e^{z_i} / Σ_j e^{z_j}`. Outputs a probability distribution
over classes. Numerically unstable if implemented naively; always use the
"subtract max" trick: `softmax(z) = softmax(z - max(z))`.

### Activation Comparison

| Activation | Range | Saturates? | Default Use |
| --- | --- | --- | --- |
| Sigmoid | (0, 1) | Yes (both ends) | Binary output |
| Tanh | (-1, 1) | Yes (both ends) | Legacy RNNs |
| ReLU | [0, ∞) | Half (negatives) | Hidden in MLPs/CNNs |
| Leaky ReLU | (-∞, ∞) | No | When dead ReLU appears |
| GELU | (-∞, ∞) | Mild | Hidden in transformers |
| SiLU | (-∞, ∞) | Mild | Hidden in modern arch |
| Softmax | (0, 1) | Yes | Multiclass output |

## Why It Matters in Real Jobs

Three reasons. First, training stability: the wrong activation can produce
vanishing or exploding gradients that prevent the network from learning.
Second, model capacity at fixed depth: GELU and SiLU are smoother than ReLU,
which sometimes helps very deep networks find better minima. Third, the
output activation is part of the loss function design: sigmoid + BCE, softmax
+ cross-entropy are standard pairings; mixing them up is a frequent bug.

In an interview, the depth of your activation knowledge signals how much
training you have done. Knowing the dead ReLU problem, the sigmoid
saturation argument, and why GELU appears in transformers separates someone
who has trained networks from someone who has only read about them.

## How It Works Step by Step

1. **Pick the output activation by task.** Sigmoid for binary classification,
   softmax for multiclass, identity for regression.
2. **Pick the hidden activation by architecture.** ReLU for CNNs and most
   MLPs. GELU or SiLU for transformers. Tanh almost never; sigmoid almost
   never.
3. **Match initialization to activation.** He initialization for ReLU and
   variants. Xavier for tanh and sigmoid.
4. **Watch for dead ReLUs.** Print histogram of activations after a few
   epochs. If many units are always zero, switch to Leaky ReLU or lower the
   learning rate.
5. **Pair the output activation with the right loss.** Sigmoid + BCE; softmax
   + cross-entropy; identity + MSE. Numerical-stability fused implementations
   (`BCEWithLogitsLoss`, `CrossEntropyLoss` in PyTorch) are preferred.
6. **Profile if necessary.** GELU and SiLU are slightly slower than ReLU.
   Rarely matters except in inference-bound serving.

## Real-World Example

A team trains a 50-layer ResNet for image classification. With sigmoid
activations and standard initialization, the gradients vanish in the first
few layers and validation accuracy is stuck at 10 percent (random). They
switch to ReLU and add He initialization plus batch normalization, and
validation accuracy rises to 92 percent. They later port the model to a ViT
(vision transformer) with GELU activations; same data, same training budget,
validation accuracy is 93.5 percent. The lesson: activation choice is
inseparable from the rest of the architecture and training recipe; copy
recipes from papers that match your architecture rather than mixing.

## Common Mistakes

- Using sigmoid or tanh in deep hidden layers; gradient vanishes.
- Using ReLU and ignoring dead units; check activation histograms.
- Implementing softmax without the max-subtraction trick; numerical overflow.
- Applying softmax twice (once in the model, once in the loss). The
  combined cross-entropy loss expects logits, not probabilities.
- Mixing sigmoid output with cross-entropy loss for multiclass. Use softmax
  + cross-entropy, or BCE with one-hot for multilabel.
- Forgetting to apply softmax at inference if the loss had it fused.
- Initializing a ReLU network with Xavier; gradients are too small in early
  training.
- Picking GELU "because transformers use it" in a small CNN where ReLU is
  fine.

## Interview Angle

**Question:** Why has ReLU largely replaced sigmoid and tanh as the default
activation in deep networks?

**Strong answer:** Three reasons.

First, **gradient flow**. Sigmoid and tanh saturate at large `|z|`, where
their derivatives drop to nearly zero. In a deep network, the chain rule
multiplies these tiny derivatives through layers, so gradients in early
layers vanish exponentially with depth. Networks beyond ~10 layers with
sigmoid or tanh barely train. ReLU has derivative 1 for all positive inputs,
so positive gradients flow without attenuation through the layers they
activate.

Second, **computational simplicity**. ReLU is a comparison and a max
operation. Sigmoid and tanh require an exponential. On modern hardware,
this is a measurable speed difference at scale.

Third, **sparse activations**. About half the units output zero on average
under random input, which acts as a mild regularizer and matches biological
plausibility better than dense outputs.

The cost of ReLU is the **dead ReLU** problem: a unit pushed into the
negative zone has zero gradient and cannot recover. Mitigations include He
initialization, lower learning rates, batch normalization, and Leaky ReLU
or its variants. In practice, with reasonable initialization and modern
training tricks, dead ReLUs are rare.

In transformers, ReLU has been replaced by GELU and SiLU, which are smoother
non-monotonic alternatives that empirically help training stability at very
large scale. The improvement over ReLU is small but consistent.

**Weak answer:** "ReLU is faster" without naming the saturation argument.

**Follow-up questions:**

- What is the dead ReLU problem and how do you mitigate it?
- Why do transformers use GELU instead of ReLU?
- How would you initialize weights for a ReLU network?
- When would you use sigmoid in a hidden layer?

## Mini Exercise

Train a 10-layer MLP on MNIST with sigmoid, tanh, and ReLU activations,
keeping everything else fixed. Plot training loss vs epoch for each. Note
how sigmoid and tanh stall while ReLU trains.

## Diagram

```mermaid
flowchart LR
    Z[Pre-activation z = W x + b] --> A{Activation}
    A -- Sigmoid --> S[(0, 1), saturates]
    A -- Tanh --> T[(-1, 1), saturates]
    A -- ReLU --> R[max(0, z), no positive saturation]
    A -- GELU/SiLU --> G[Smooth non-monotonic]
    S --> H[Output to next layer]
    T --> H
    R --> H
    G --> H
```

---
## Navigation

[⬅ Previous](02-perceptrons-and-mlps.md) | [🏠 Home](../README.md) | [➡ Next](04-forward-propagation.md)
