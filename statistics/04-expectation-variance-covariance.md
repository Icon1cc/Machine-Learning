# Expectation, Variance, and Covariance

## Beginner-Friendly Intuition

Expectation is the long-run average. Variance is how spread out the values are. Covariance is how two variables move together. These three summaries appear in nearly every ML formula: loss is an expectation, regularization controls variance, PCA decomposes covariance.

## Formal Explanation

`E[X] = Σ x p(x)` (or `∫ x f(x) dx`). Linearity: `E[aX + bY] = aE[X] + bE[Y]`. `Var(X) = E[(X - E[X])²] = E[X²] - E[X]²`. `Var(aX + b) = a² Var(X)`. Covariance `Cov(X, Y) = E[(X - E[X])(Y - E[Y])]`; correlation `ρ = Cov(X, Y) / (σ_X σ_Y)`, in `[-1, 1]`. For independent variables, `Var(X + Y) = Var(X) + Var(Y)`.

## Why It Matters in Real Jobs

Empirical loss is a sample estimate of expectation; bias-variance decomposition is in the same language. Feature correlation explains why models do not improve when you add a near-duplicate feature. Risk dashboards report variance and covariance to capture portfolio behavior.

## How It Works Step by Step

1. Pick the quantity whose expectation you care about.
2. Compute or estimate it from data.
3. Compute variance to know how reliable that estimate is.
4. Compute covariance/correlation between features to spot redundancy.
5. Decide whether dependencies require modeling adjustments (multivariate distributions, decorrelation).

## Real-World Example

A model uses two features that are 0.95 correlated. Performance does not improve over using one. Removing the duplicate keeps performance the same and simplifies the model. Inspecting covariance saved time and complexity.

## Worked Example: Variance via `E[X²] - E[X]²`

Let `X` be uniform on `{1, 2, 3}` so each value has probability `1/3`. Then `E[X] = (1 + 2 + 3) / 3 = 2`. And `E[X²] = (1 + 4 + 9) / 3 = 14 / 3 ≈ 4.667`. Variance via the shortcut `E[X²] - E[X]²` is `14/3 - 4 = 2/3`. Cross-check via the direct definition `E[(X - E[X])²]`: `((1-2)² + (2-2)² + (3-2)²) / 3 = (1 + 0 + 1) / 3 = 2/3`. They match. The shortcut is what frameworks use internally because it requires only running sums of `x` and `x²`, not a second pass over the data.

## Worked Example: Covariance Matrix from a Tiny Dataset

Three observations of two features:

| Row | X | Y |
| --- | --- | --- |
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 6 |

Means: `E[X] = 2`, `E[Y] = 4`. Centered values for `(X, Y)`: `(-1, -2), (0, 0), (1, 2)`.

- `Var(X) = ((-1)² + 0² + 1²) / 3 = 2/3`
- `Var(Y) = ((-2)² + 0² + 2²) / 3 = 8/3`
- `Cov(X, Y) = ((-1)(-2) + 0 + (1)(2)) / 3 = 4/3`

Covariance matrix `Σ = [[2/3, 4/3], [4/3, 8/3]]`. Correlation `ρ = Cov(X,Y) / sqrt(Var(X) Var(Y)) = (4/3) / sqrt(2/3 * 8/3) = (4/3) / (4/3) = 1`. Perfect linear relationship, as expected since `Y = 2X` exactly. Note that this calculation uses the population variance with denominator `n`; the unbiased sample estimator uses `n - 1`. For `n = 3` the difference is large; for `n` in the thousands it is negligible.

## Common Mistakes

- Confusing correlation 0 with independence (it implies independence only for joint Gaussians).
- Reporting mean without variance for noisy metrics.
- Treating high correlation as causation.
- Ignoring covariance when combining models or features.

## Interview Angle

**Question:** What is the difference between correlation and causation, and when does correlation imply independence?

**Strong answer:** Correlation measures linear association; causation requires a directional, mechanistic link. Zero correlation does not imply independence in general (a quadratic relationship has zero linear correlation). It does imply independence for joint Gaussian variables. To establish causation, you need controlled experiments or careful causal inference.

**Weak answer:** Treat correlation and independence as the same.

**Follow-up questions:**

- Why does adding correlated features rarely help a linear model?
- How do you compute the covariance matrix from a data matrix?
- What is conditional expectation and where does it appear in ML?
- How does Jensen's inequality relate `E[f(X)]` and `f(E[X])`?

## Mini Exercise

Take any feature matrix. Compute the correlation matrix. List the top three highly correlated pairs and decide whether to drop or transform them.

## Diagram

```mermaid
flowchart LR
    X[Random variable] --> E[Mean E[X]]
    X --> V[Variance Var(X)]
    Y[Other variable] --> C[Cov(X,Y)]
    X --> C
    C --> Cor[Correlation ρ]
```

---
## Navigation

[⬅ Previous](03-common-distributions.md) | [🏠 Home](../README.md) | [➡ Next](05-bayes-theorem.md)
