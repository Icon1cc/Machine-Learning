# Principal Component Analysis (PCA)

## Beginner-Friendly Intuition

PCA finds the directions in your data along which the variance is largest. The
first principal component is the single direction that captures the most
variance; the second is the direction (perpendicular to the first) that
captures the most of what remains; and so on. Project your data onto the top
`k` components and you have a lower-dimensional version that keeps as much of
the original spread as possible.

The intuition is geometric. Imagine a 3D scatterplot of points that mostly lie
on a tilted plane. PCA finds that plane. The first two components span it; the
third (perpendicular to it) captures only the tiny variation away from the
plane. Drop the third and you have a faithful 2D representation.

PCA is one of the oldest and most-used tools in ML. It does dimensionality
reduction, decorrelation, visualization, denoising, and feature compression.
It is also linear (it can only find linear structure), variance-based (which
is not always meaningful), and easy to misuse on data that violates its
assumptions.

## Formal Explanation

Given a centered data matrix `X ∈ R^{n × d}` (each column has zero mean), PCA
computes the eigendecomposition of the sample covariance matrix
`Σ = (1/n) X^T X`:

```
Σ = V Λ V^T
```

where `V ∈ R^{d × d}` is the orthonormal matrix of eigenvectors (the principal
components) and `Λ` is the diagonal matrix of eigenvalues sorted in
descending order. The eigenvectors point in the directions of maximum
variance; the eigenvalues are the variances along those directions.

Equivalently, PCA is the **truncated SVD** of `X`:

```
X = U S V^T
```

where the columns of `V` are the principal components, the singular values
`s_i = sqrt(λ_i n)` capture the variance, and the projections of `X` onto the
components are `X V`. Truncating to the top `k` components gives the
best rank-`k` approximation of `X` in Frobenius norm (Eckart-Young theorem).

**Explained variance.** Component `i` explains `λ_i / Σ_j λ_j` of the total
variance. The cumulative explained variance grows as you add components; pick
`k` so the cumulative reaches 85, 90, or 95 percent depending on your
tolerance for information loss.

**The scree plot.** Plot eigenvalues `λ_i` against `i`. There is often a
natural elbow: the eigenvalues drop quickly for the first few components and
then plateau. The elbow is a heuristic for choosing `k`.

**Standardization.** PCA is **scale-sensitive**. Always standardize features
first (subtract mean, divide by std) unless every feature is already on the
same scale and that scale is meaningful. Without standardization, a feature in
[0, 1000] dominates a feature in [0, 1].

**Variants.**

- **Kernel PCA.** Apply PCA in the implicit feature space of a kernel.
  Discovers non-linear structure (e.g., points on a circle become a line in
  kernel space). Useful when linear PCA underfits.
- **Sparse PCA.** Adds an L1 penalty on the loadings. Each component has
  exactly-zero entries on most features, making components interpretable. Loses
  some variance.
- **Incremental PCA.** Streaming version that does not require holding `X` in
  memory.
- **Probabilistic PCA.** Bayesian formulation. Useful when handling missing
  values or building generative models.

## Why It Matters in Real Jobs

Three production roles. First, **dimensionality reduction for downstream
models**: project a 1000-feature dataset to 50 PCA components, train a
classifier on the projection. Often nearly as accurate as training on the full
features, with substantially faster fitting and inference. Especially useful
for k-means and KNN, which struggle in high dimensions. Second, **noise
reduction**: low-variance components often capture noise; reconstructing from
the top `k` components denoises the data. Used in image processing, financial
time series, and EEG. Third, **visualization**: project to 2D or 3D and plot.
Almost every data exploration session has a PCA scatter at some point.

PCA loses when the structure is non-linear (use Kernel PCA, t-SNE, UMAP, or
autoencoders), when interpretability per feature matters (use sparse PCA or
factor analysis), or when the directions of maximum variance are not the
directions of maximum signal (e.g., classification, where between-class
variance matters; use LDA instead).

## How It Works Step by Step

1. **Standardize features.** Subtract mean, divide by standard deviation per
   column.
2. **Compute the SVD or eigendecomposition.** sklearn `PCA(n_components=k)`.
3. **Pick `k`.** Look at the cumulative explained variance and pick the
   smallest `k` that exceeds your threshold (often 85, 90, or 95 percent).
4. **Inspect the scree plot.** Look for an elbow as a sanity check.
5. **Read the loadings.** Each principal component is a weighted combination
   of original features. Look at which features dominate each component for
   interpretation.
6. **Project and use.** `X_pca = X_centered @ V_k`. Use as features for the
   downstream model.
7. **Validate that the projection preserves what matters.** Compare downstream
   model performance on the full features vs the PCA features. If the gap is
   large, `k` is too small or the structure is non-linear.

## Real-World Example

A team has a tabular dataset with 480 features built from raw event logs. The
top 20 features look meaningful; the rest are derived counts, ratios, and
rolling aggregates that overlap heavily. They standardize and run PCA.
Cumulative explained variance hits 95 percent at `k = 47`. They train their
gradient boosted model on the 47 PCA components and on the original 480
features. AUC differs by 0.003. They ship the PCA pipeline because training
time drops 6x, model size drops 9x, and inference latency drops by half.
Inspecting the top three components reveals they correspond to "overall
activity volume", "time-of-day pattern", and "category diversity" -- which
the team uses as engineered features in a more interpretable model variant.

## Common Mistakes

- Skipping standardization on features with very different scales. The
  largest-scale feature dominates every component.
- Applying PCA before splitting train and test, leaking test statistics into
  the projection.
- Using the wrong number of components by reading the scree plot only;
  cumulative explained variance is the more honest criterion.
- Treating PCA components as causally meaningful. They are linear combinations
  of the original features chosen for variance.
- Running PCA on classification problems and being surprised that the top
  components do not separate classes. PCA optimizes variance, not class
  separation. Use LDA for the latter.
- Using PCA on non-linear data (e.g., points on a circle) and getting useless
  reductions. Kernel PCA, autoencoders, or UMAP handle non-linearity.
- Forgetting that PCA is sensitive to outliers; one extreme point can rotate
  the top component dramatically. Pre-process to remove or winsorize.
- Picking `k` so high that PCA does nothing useful. If `k = d` you have just
  rotated your data.

## Interview Angle

**Question:** Why do we standardize features before applying PCA, and what
goes wrong if we do not?

**Strong answer:** PCA seeks directions of maximum variance in the input
features. If features are on very different scales (e.g., income in dollars
ranging from 0 to 200,000 and age in years ranging from 18 to 80), the
variance in income is roughly 10^9 and the variance in age is roughly 10^2.
The first principal component will be almost exactly aligned with income,
because that is where almost all the variance lives, even if income is no
more meaningful than age for the underlying problem. Standardizing each
feature to mean 0 and standard deviation 1 puts every feature on the same
variance footing, so PCA finds directions that genuinely combine information
across features rather than trivially picking the largest-scale one.
Mathematically, this is equivalent to running PCA on the correlation matrix
instead of the covariance matrix. The exception is when every feature is
already on the same physical scale and the relative magnitudes are
meaningful (e.g., all features are pixel intensities in [0, 255]); there
standardization can hurt by destroying meaningful scale differences.

**Weak answer:** "Standardization is good practice" without explaining what
goes wrong without it.

**Follow-up questions:**

- What is the relationship between PCA and SVD?
- How do you choose `k`?
- When does PCA fail and what would you use instead?
- What is the difference between PCA and LDA?

## Mini Exercise

Take a tabular dataset with at least 50 numeric features. Standardize. Fit PCA
with all components. Plot the cumulative explained variance vs `k`. Mark the
`k` for 90 percent and 95 percent. Train a logistic regression on the top
20 components and on the full features; compare AUC.

## Diagram

```mermaid
flowchart LR
    X[Centered, standardized X] --> S[Compute SVD: X = U S V^T]
    S --> V[Top k components V_k]
    V --> P[Project: X_k = X V_k]
    P --> D[Downstream model or visualization]
```

---
## Navigation

[⬅ Previous](12-dbscan.md) | [🏠 Home](../README.md) | [➡ Next](14-anomaly-detection.md)
