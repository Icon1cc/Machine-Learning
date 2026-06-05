# Information Theory: Entropy, Cross-Entropy, and KL Divergence

## Beginner-Friendly Intuition

Entropy measures how uncertain a distribution is. Cross-entropy measures how badly one distribution predicts another. KL divergence measures the extra cost of using the wrong distribution to encode the right one. Most classification losses are cross-entropy; many regularizers and alignment losses are KL divergences.

## Formal Explanation

For a distribution `p`, entropy is `H(p) = -Σ p(x) log p(x)`. Cross-entropy of `q` relative to `p` is `H(p, q) = -Σ p(x) log q(x)`. KL divergence is `KL(p || q) = Σ p(x) log(p(x) / q(x)) = H(p, q) - H(p)`. KL is non-negative and zero iff `p = q`. It is asymmetric: `KL(p || q) != KL(q || p)`. In ML, `p` is the target (one-hot or soft label), `q` is the model's predicted distribution.

## Why It Matters in Real Jobs

Cross-entropy is the standard loss for classification because it directly penalizes confident wrong predictions. KL divergence underlies label smoothing, knowledge distillation (student predicts teacher), variational autoencoders, and policy regularization in RLHF. Calibration metrics are entropy-based.

## How It Works Step by Step

1. For a hard-labeled classification, cross-entropy reduces to `-log p(true class)`.
2. Use softmax to map logits to a distribution before computing cross-entropy.
3. Use KL when both target and prediction are full distributions (distillation, RLHF).
4. Use label smoothing to soften targets and improve calibration.
5. Track per-class cross-entropy to see which classes the model is bad at.

## Real-World Example

A model is overconfident on training data and miscalibrated. Adding label smoothing (target becomes `(1-ε) one_hot + ε/K uniform`) is equivalent to training against a softer KL target. The model becomes less confident, generalizes better on validation, and produces probabilities that match observed frequencies.

## Common Mistakes

- Confusing entropy (a property of one distribution) with cross-entropy (between two).
- Treating KL as a distance even though it is not symmetric and does not satisfy the triangle inequality.
- Forgetting that cross-entropy with one-hot targets equals `-log p(true)`.
- Using KL when forward and reverse give different answers without thinking about which to pick.

## Forward vs Reverse KL: Mode-Covering vs Mode-Seeking

Forward KL `KL(p || q)` is the standard form: `p` is the truth, `q` is the approximation. The integrand is `p log(p/q)`, which goes to infinity wherever `p > 0` and `q ≈ 0`. To avoid that infinity, `q` must put mass everywhere `p` does. The result is **mode-covering**: `q` smears its mass to cover every mode of `p`, even if it ends up putting mass in low-density regions in between. Maximum likelihood training minimizes forward KL of the data distribution to the model.

Reverse KL `KL(q || p)` swaps the arguments. The integrand is `q log(q/p)`, which goes to infinity wherever `q > 0` and `p ≈ 0`. To avoid that, `q` must avoid putting mass where `p` is small. The result is **mode-seeking**: `q` focuses on one mode of `p` and ignores the others. Variational inference (the typical VAE objective) minimizes reverse KL of the approximate posterior to the true posterior, which is why VAE-style approximations often collapse to a single mode. Policy distillation in some RL setups also uses reverse KL, and the mode-seeking property is sometimes desired because the policy must commit to one action.

Concrete picture: if `p` is a bimodal distribution (two Gaussians) and `q` is constrained to be a single Gaussian, forward KL puts `q` in the middle, covering both modes (poor fit at either mode but mass everywhere). Reverse KL puts `q` on one of the two modes (sharp fit at one mode, ignores the other).

## Softmax Temperature

Adding a temperature `T` to softmax gives `softmax_i(z) = exp(z_i / T) / Σ_j exp(z_j / T)`. As `T -> 0`, the distribution concentrates on the argmax (entropy goes to zero, like a hard one-hot). As `T -> ∞`, it becomes uniform (entropy goes to `log K`). Temperature is the most direct way to control entropy at inference time. In knowledge distillation, the teacher's outputs are softened with `T > 1` so the student sees the relative ranking among the non-top classes, which is where most of the dark knowledge lives. In RLHF and language model sampling, `T = 0.7` to `1.0` controls the exploration-exploitation trade-off, and `T = 0` (greedy) is what you want for deterministic generation.

## Interview Angle

**Question:** Explain entropy, cross-entropy, and KL divergence and how each shows up in an ML loss.

**Strong answer:** Entropy is the average information needed to encode samples from a distribution. Cross-entropy is the cost of encoding samples from `p` using a code optimized for `q`. KL is the difference: how much extra you pay using `q` instead of the true `p`. In ML, classification loss is cross-entropy with the model's predicted distribution; distillation uses KL of student to teacher; label smoothing softens the target; VAEs penalize KL of approximate posterior to prior.

**Weak answer:** Quote formulas without explaining what each measures or how it is used.

**Follow-up questions:**

- Why is forward KL `KL(p || q)` mode-covering and reverse KL mode-seeking?
- How does temperature in softmax affect entropy?
- How is KL related to maximum likelihood estimation?
- What is mutual information and how is it related?

## Mini Exercise

Compute entropy, cross-entropy, and KL for two simple discrete distributions by hand. Verify `KL(p || q) = H(p, q) - H(p)`.

## Diagram

```mermaid
flowchart LR
    P[True dist p] --> CE[Cross-entropy H(p,q)]
    Q[Pred dist q] --> CE
    P --> H[Entropy H(p)]
    CE --> KL[KL = H(p,q) - H(p)]
    H --> KL
```

---
## Navigation

[⬅ Previous](10-convex-vs-non-convex-optimization.md) | [🏠 Home](../README.md) | [➡ Next](12-distance-metrics.md)
