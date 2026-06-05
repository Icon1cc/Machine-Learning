# Eigenvalues, Eigenvectors, and the Intuition Behind PCA

## Beginner-Friendly Intuition

An eigenvector of a matrix is a direction that does not get rotated by the matrix; only stretched. The stretch factor is the eigenvalue. PCA finds the directions in which data varies most. Those are the eigenvectors of the covariance matrix, and the variance along each is the eigenvalue. Compressing a dataset to its top eigenvectors keeps the information you care about with fewer dimensions.

## Formal Explanation

If `A v = λ v` for nonzero `v`, then `v` is an eigenvector of `A` with eigenvalue `λ`. For a real symmetric matrix (like a covariance matrix), eigenvectors are orthogonal and eigenvalues are real. PCA centers data, computes covariance `Σ = X^T X / n`, and decomposes it. The principal components are the eigenvectors sorted by eigenvalue. Equivalently, SVD of the centered data matrix gives the same components.

## Why It Matters in Real Jobs

PCA is the simplest, fastest dimensionality reduction. It is used to visualize, denoise, compress, decorrelate features, and as a starting point before training. Eigen-decomposition also underlies spectral clustering, PageRank, and many graph methods. It is one of the most transferable mental models in math for ML.

## How It Works Step by Step

1. Center the data (subtract the mean per feature).
2. Compute the covariance matrix (or SVD on the centered data).
3. Sort eigenvalues from largest to smallest.
4. Keep the top k components that explain enough variance (often 90 or 95 percent).
5. Project data onto those components for the reduced representation.

## Real-World Example

A model has 200 highly correlated features. Training is slow and unstable. Running PCA reveals 95 percent of variance in the top 30 components. Training on those is faster, more stable, and only loses a tiny fraction of accuracy. Storage and inference also drop.

## Common Mistakes

- Forgetting to center the data; PCA without centering captures the mean direction.
- Using PCA on highly nonlinear structure (consider kernel PCA or autoencoders).
- Treating principal components as interpretable features without checking.
- Applying PCA before splitting train/validation, leaking statistics.
- Keeping too few components and losing important variance.

## Interview Angle

**Question:** Explain PCA in terms of eigenvalues and how you would choose the number of components.

**Strong answer:** PCA finds orthogonal directions that maximize variance. They are the top eigenvectors of the (centered) covariance matrix. Pick `k` by the cumulative explained variance, e.g. 90 or 95 percent, or by an elbow in the variance curve. Always fit PCA on training data only and apply it to validation.

**Weak answer:** Confuse PCA with feature selection or apply it without centering.

**Follow-up questions:**

- When is PCA a bad fit?
- How does SVD relate to eigen-decomposition?
- What is whitening and when do you want it?
- How does kernel PCA differ from PCA?

## Mini Exercise

Take a tabular dataset. Run PCA, plot the cumulative explained variance, pick the elbow, and report how much variance the top components capture. Then train any model on the reduced set and compare to the full features.

## Diagram

```mermaid
flowchart LR
    X[Centered data X] --> C[Covariance Σ]
    C --> E[Eigen-decompose]
    E --> V[Top-k eigenvectors]
    X --> P[Project to V]
    V --> P
    P --> R[Reduced representation]
```

---
## Navigation

[⬅ Previous](04-dot-products-projections-and-similarity.md) | [🏠 Home](../README.md) | [➡ Next](06-calculus-derivatives.md)
