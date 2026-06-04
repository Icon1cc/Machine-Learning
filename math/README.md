# Math

## Folder Purpose

Linear algebra, calculus, optimization, distance metrics, and information theory for machine learning.

## Beginner Intuition

You do not need to be a mathematician to do ML, but three ideas keep showing up. Linear algebra moves
and combines data (a neural layer is a matrix multiply). Calculus tells you which direction reduces
error (the gradient). Probability and information theory let you write loss functions and reason about
uncertainty. Learn what each tool computes and why, not every proof.

## Why It Matters

When training diverges, stalls, or a loss does not move, the cause is usually mathematical: a learning
rate that overshoots, gradients that vanish through depth, or a loss that is not what you think it is.
The math is what lets you diagnose instead of guess.

## Who Should Read This Section

Read this if formulas in other sections feel like magic, or if you can call library functions but
cannot explain why softmax uses exponentials or what PCA optimizes. It is the toolkit the rest of the
curriculum leans on.

## Recommended Reading Order

Read in order: vectors and matrices first, then dot products and eigenvectors, then derivatives and
gradients, then optimization, then information theory and distance metrics. Each builds on the last.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Why Math Matters For ML](01-why-math-matters-for-ml.md) |
| 2 | [Linear Algebra Vectors](02-linear-algebra-vectors.md) |
| 3 | [Matrices And Matrix Multiplication](03-matrices-and-matrix-multiplication.md) |
| 4 | [Dot Products Projections And Similarity](04-dot-products-projections-and-similarity.md) |
| 5 | [Eigenvalues Eigenvectors And PCA Intuition](05-eigenvalues-eigenvectors-and-pca-intuition.md) |
| 6 | [Calculus Derivatives](06-calculus-derivatives.md) |
| 7 | [Gradients And Partial Derivatives](07-gradients-and-partial-derivatives.md) |
| 8 | [Chain Rule And Backpropagation Intuition](08-chain-rule-and-backpropagation-intuition.md) |
| 9 | [Optimization Gradient Descent](09-optimization-gradient-descent.md) |
| 10 | [Convex Vs Non Convex Optimization](10-convex-vs-non-convex-optimization.md) |
| 11 | [Information Theory Entropy Cross Entropy Kl Divergence](11-information-theory-entropy-cross-entropy-kl-divergence.md) |
| 12 | [Distance Metrics](12-distance-metrics.md) |

## Real-World Examples

- Cosine similarity (a dot product of normalized vectors) powers semantic search and recommendations.
- Gradient descent is the update rule behind essentially every trained model.
- Cross-entropy, an information-theory quantity, is the standard classification and language-modeling
  loss.
- PCA (eigenvectors of the covariance matrix) compresses features and denoises data.

## Pattern Recognition

- "Loss exploded to NaN" points to learning rate or numerical stability (subtract the max in softmax).
- "Deep network will not learn" points to vanishing gradients (chain rule through many layers).
- "Need to compare two vectors" points to a distance or similarity metric choice.
- "Reduce dimensions" points to PCA and eigenvectors.

## Common Mistakes

- Thinking the gradient points toward the minimum (it points uphill; descent subtracts it).
- Forgetting softmax is shift-invariant, so subtracting the max prevents overflow.
- Treating any non-convex loss as hopeless instead of expecting good local minima.
- Using the wrong distance metric for the embedding space.

## Interview Notes

Expect "derive the gradient of MSE", "explain backprop with the chain rule", "why exponentials in
softmax", "what does PCA optimize", "cross-entropy vs KL divergence". Pair each formula with one
sentence of meaning.

## What You Should Know After Finishing

- How a linear layer, a gradient, and a loss connect into the training loop.
- Why scaling and similarity metrics depend on dot products and norms.
- How the chain rule produces backpropagation.
- What entropy, cross-entropy, and KL divergence measure.

## Suggested Exercises

- Derive the gradient of `(y - wx)^2` with respect to `w` by hand.
- Compute the cosine similarity of two small vectors and interpret it.
- Explain in plain words why dividing attention scores by sqrt(d) helps.
- Work one PCA example and state what the top component captures.

## Navigation

[🏠 Home](../README.md)
