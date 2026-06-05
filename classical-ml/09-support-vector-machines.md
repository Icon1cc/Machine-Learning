# Support Vector Machines

## Beginner-Friendly Intuition

A support vector machine finds the line (or hyperplane in higher dimensions)
that separates two classes with the **widest possible gap** between them. The
points that sit on the edge of that gap are the support vectors; everything
else is irrelevant. The intuition is geometric: among all hyperplanes that
correctly classify the data, pick the one with the most breathing room on
either side. More margin equals better generalization.

The reason to learn SVMs even though they have largely been replaced by
gradient boosting on tabular data and deep learning on images: SVMs introduced
the **kernel trick**, which lets you compute dot products in arbitrarily
high-dimensional spaces without ever materializing those spaces. That idea
shaped a generation of ML and is still useful today for small-data problems
with non-linear structure.

## Formal Explanation

For a binary classification problem with labels `y_i ∈ {-1, +1}`, the
**hard-margin** SVM solves:

```
minimize  0.5 ||w||²
subject to  y_i (w · x_i + b) >= 1   for all i
```

The decision rule is `sign(w · x + b)`. The margin width is `2 / ||w||`;
maximizing margin means minimizing `||w||`. The constraints force every point
to be at least distance `1 / ||w||` from the boundary on the correct side.

For data that is not linearly separable, the **soft-margin** SVM allows
violations through slack variables `ξ_i >= 0`:

```
minimize  0.5 ||w||² + C Σ ξ_i
subject to  y_i (w · x_i + b) >= 1 - ξ_i,   ξ_i >= 0
```

The hyperparameter `C` controls the trade-off between margin width and
violations. Large `C`: penalize errors heavily, narrower margin. Small `C`:
tolerate errors, wider margin (more regularization).

The **dual formulation** rewrites the optimization in terms of Lagrange
multipliers `α_i`:

```
maximize  Σ α_i - 0.5 Σ_{i,j} α_i α_j y_i y_j (x_i · x_j)
subject to  0 <= α_i <= C,   Σ α_i y_i = 0
```

In the dual, only **dot products** `x_i · x_j` appear. The decision function is
`f(x) = sign(Σ α_i y_i (x_i · x) + b)`. Most `α_i` are zero; only support
vectors contribute.

### The Kernel Trick

Replace `x_i · x_j` with `K(x_i, x_j)`, where `K` is a kernel function that
implicitly computes a dot product in some higher-dimensional feature space
`φ(x)`. You never compute `φ` explicitly. Common kernels:

- **Linear:** `K(x, x') = x · x'`. Equivalent to no kernel.
- **Polynomial:** `K(x, x') = (γ x · x' + r)^d`. Captures interactions up to
  degree `d`.
- **RBF (Gaussian):** `K(x, x') = exp(-γ ||x - x'||²)`. The default non-linear
  kernel; `γ` controls how local each support vector's influence is.
- **Sigmoid:** `K(x, x') = tanh(γ x · x' + r)`.

`γ` and `C` are the two RBF-SVM hyperparameters that matter. Tune jointly.

### SVM regression (SVR)

Same idea, but the loss is the **ε-insensitive loss**: errors smaller than `ε`
contribute nothing, errors larger than `ε` are penalized linearly. This produces
a "tube" of width `2ε` around the regression line where points cost zero.

## Why It Matters in Real Jobs

In 2026, SVMs are not the first model anyone reaches for. Gradient boosted
trees beat RBF-SVMs on most tabular data with less tuning, and deep networks
beat them on unstructured data by a much larger margin. So why teach them?
Three reasons.

First, SVMs remain a strong baseline for small-data problems (under ~5K rows)
with a clear non-linear structure. Their explicit margin maximization gives a
useful inductive bias when overfitting risk is high.

Second, the kernel trick is conceptually critical. Kernel methods underlie
Gaussian processes (which are the modern Bayesian non-parametric regression
tool), spectral clustering, and many similarity-based methods. Understanding
SVMs lets you read these.

Third, SVMs are still used in some production niches: text classification on
small labeled sets (linear SVMs with TF-IDF), bioinformatics (RBF kernels on
small N, large d data), and as the final-layer classifier on top of frozen
deep features in some legacy systems.

## How It Works Step by Step

1. **Standardize features.** SVM is scale-sensitive (RBF kernel especially).
2. **Try a linear SVM first.** `LinearSVC` or `SVC(kernel='linear')`. Cheap
   baseline.
3. **If non-linear structure is present, switch to RBF.** Tune `C` and `γ`
   jointly with grid search or randomized search. Typical sweep: `C ∈
   {0.1, 1, 10, 100}`, `γ ∈ {0.001, 0.01, 0.1, 1} / d` where `d` is feature
   count.
4. **Watch for training-time blow-up.** SVM training is `O(n² d)` to `O(n³ d)`.
   Above 50K rows, switch to a linear SVM with stochastic optimization
   (`sklearn.svm.LinearSVC`) or a different model (GBM, neural net) entirely.
5. **Calibrate.** SVMs do not output probabilities natively. Use Platt scaling
   (sigmoid fit on validation) or the `probability=True` flag in sklearn,
   which does this internally and is slow.
6. **Inspect support vectors.** A high fraction of the training set being
   support vectors signals overfitting (tighter `C`) or noisy data.

## Why SVMs Lost Ground

Three reasons. First, training cost: SVM training scales superlinearly with
data, while GBMs and neural networks scale linearly. By 2010, datasets had
grown past the size where SVM training was practical. Second, calibration: SVM
decision values are not probabilities, requiring a post-hoc calibration step
(Platt scaling) that can introduce its own bias. Third, automatic feature
learning: SVMs require kernels chosen by hand, while neural networks learn
representations from raw data. Once GPUs made deep learning practical for
images and text, the kernel idea was supplanted by learned features.

## Real-World Example

A small biology lab has 1,200 samples of gene expression measurements (12K
features per sample) and a binary disease label. With more features than
samples and no obvious linear separability, they try three models. Logistic
regression with strong L2 reaches 0.78 AUC. A random forest with 500 trees
reaches 0.81. An RBF SVM with `C = 10`, `γ = 1 / (12000 * 0.5)` (sklearn
default scaled by 0.5) reaches 0.85. The SVM wins because the data is small
and the inductive bias of margin maximization plus an RBF kernel matches the
problem better than the trees can with so little data. They ship the SVM with
Platt-scaled probabilities. The team would not use SVM if they had 100K
samples; on small data, it earned its place.

## Common Mistakes

- Skipping standardization. SVMs are scale-sensitive; a feature in [0, 1000]
  dominates RBF distances over a feature in [0, 1].
- Using `kernel='rbf'` on a million-row dataset and waiting for training to
  finish.
- Tuning `C` without `γ`, or vice versa. They interact strongly.
- Treating decision values as calibrated probabilities.
- Using `probability=True` in sklearn for production scoring; it is slow and
  refits Platt scaling internally. Calibrate explicitly with `CalibratedClassifierCV`.
- Forgetting that SVM is a binary classifier by default; multiclass via
  one-vs-rest or one-vs-one increases cost.
- Comparing SVM accuracy to a poorly-tuned GBM and concluding SVM wins. Tune
  both fairly.

## Interview Angle

**Question:** Explain the kernel trick and why it allows SVMs to learn
non-linear boundaries without computing the high-dimensional feature mapping
explicitly.

**Strong answer:** The dual SVM optimization depends on the data only through
dot products `x_i · x_j`. So if we mapped each input through some non-linear
function `φ(x)` into a higher-dimensional space, the optimization would only
need `φ(x_i) · φ(x_j)`. The kernel trick is the observation that for many
useful `φ`, this inner product can be computed directly from the original
inputs via a kernel function `K(x_i, x_j)` without ever materializing `φ`. For
example, the RBF kernel `K(x, x') = exp(-γ ||x - x'||²)` corresponds to an
infinite-dimensional `φ` (a sum of Gaussians at every possible center), and yet
each kernel evaluation costs `O(d)`. So we get the expressive power of an
infinite-dimensional model with finite computation. The decision function is a
weighted sum of kernel evaluations against support vectors, which preserves
that efficiency at inference too.

**Weak answer:** "It maps to a higher dimension" without explaining why we
never compute that mapping.

**Follow-up questions:**

- What does `C` control and what does `γ` control in an RBF SVM?
- Why does SVM scale poorly with data size?
- How do you get probabilities from an SVM?
- When would you pick a linear SVM over logistic regression?

## Mini Exercise

Generate a 2D synthetic dataset with two interleaved spirals. Fit a linear SVM,
an RBF SVM with `γ = 0.1`, and an RBF SVM with `γ = 10`. Plot the decision
boundary for each. Explain how `γ` controls locality.

## Diagram

```mermaid
flowchart LR
    X[Features x] --> K[Kernel K(x, x_i)]
    SV[Support vectors] --> K
    K --> S[Σ α_i y_i K(x, x_i) + b]
    S --> D[Decision: sign or threshold]
```

---
## Navigation

[⬅ Previous](08-xgboost-lightgbm-catboost.md) | [🏠 Home](../README.md) | [➡ Next](10-k-means-clustering.md)
