# Maximum Likelihood Estimation

## Beginner-Friendly Intuition

MLE picks the parameters that make the observed data most likely under the assumed model. It is the workhorse of training: classification with cross-entropy is MLE, regression with MSE is MLE under Gaussian noise, and many other losses are MLEs of specific likelihoods.

## Formal Explanation

Given a parametric model `p(x; θ)` and i.i.d. data `x_1, ..., x_n`, the likelihood is `L(θ) = Π p(x_i; θ)`. The log-likelihood `ℓ(θ) = Σ log p(x_i; θ)` is easier to optimize. MLE is `θ_hat = argmax ℓ(θ)`, often by setting the gradient to zero or running gradient descent. Under regularity conditions, MLE is consistent and asymptotically efficient.

## Why It Matters in Real Jobs

Most ML losses are negative log-likelihoods. Knowing the underlying likelihood tells you which loss to use, what the model assumes about the noise, and what the maximum-likelihood asymptotics imply about confidence intervals.

## How It Works Step by Step

1. Choose a probabilistic model that matches the data.
2. Write the log-likelihood as a sum over data points.
3. Take the derivative with respect to parameters.
4. Set to zero (closed form) or run gradient descent (general case).
5. Validate that the assumed distribution actually fits the data.

## Real-World Example

Linear regression with squared error is MLE under the assumption that residuals are i.i.d. Gaussian. If residuals are heavy-tailed, MLE under a Laplace distribution gives least absolute deviations, which is more robust. Choosing the right likelihood is choosing the right loss.

## MLE Bias: The Gaussian Variance

MLE is consistent (it converges to the true parameter as `n -> ∞`) but it is not always unbiased for finite `n`. The classic example: the MLE of the variance of a Gaussian is `(1/n) Σ (x_i - x_bar)²`, but the unbiased estimator divides by `n - 1` instead of `n`. The reason: using the sample mean `x_bar` instead of the true mean reduces the sum of squared deviations by exactly the right amount to make the `1/n` version underestimate the variance on average. The bias factor is `(n-1)/n`. For `n = 10`, the MLE is 10 percent too low on average; for `n = 100`, only 1 percent too low. For large samples it does not matter; for small samples, divide by `n - 1`. NumPy's `var()` defaults to `n` (MLE), Pandas defaults to `n - 1` (unbiased). Knowing the convention prevents confusion.

## MLE vs MAP and the L1 Connection

MAP (maximum a posteriori) adds a prior to MLE. Instead of maximizing the likelihood, you maximize `log p(data | θ) + log p(θ)`. The prior acts as regularization. Two important cases:

- **Gaussian prior on weights.** `log p(θ) = -λ ||θ||² + const`. Adding this to the likelihood gives the same objective as MLE plus L2 (ridge) regularization. So L2 is MAP with a Gaussian prior.
- **Laplace prior on weights.** `log p(θ) = -λ ||θ||_1 + const`. Adding gives MLE plus L1 (lasso) regularization. So L1 is MAP with a Laplace prior. The Laplace prior is sharply peaked at zero, which is why L1 produces sparse solutions: the prior actively prefers exactly-zero coefficients.

The practical takeaway: regularization is not an ad-hoc trick; it is Bayesian inference under a specific prior. Choosing L1 vs L2 is choosing whether you believe most coefficients should be exactly zero (Laplace) or just small (Gaussian).

## Common Mistakes

- Using MSE on classification (wrong likelihood).
- Forgetting that MLE can overfit small data; regularization or MAP is safer.
- Quoting MLE confidence intervals without checking the model fits.
- Believing MLE is always unbiased; it can be biased for small samples.

## Interview Angle

**Question:** Explain MLE and connect it to the cross-entropy loss in classification.

**Strong answer:** MLE picks parameters that maximize `Σ log p(y_i | x_i; θ)`. For categorical `y` with model probability `q(y | x)`, the negative log-likelihood is `-Σ log q(y_i | x_i)`, which is exactly cross-entropy with a one-hot target. So minimizing cross-entropy is MLE for the categorical model.

**Weak answer:** Treat MLE as an unrelated theoretical concept.

**Follow-up questions:**

- What is MAP and how does it differ from MLE?
- When is MLE biased?
- What is the connection between MLE and KL divergence?
- Why is regularization equivalent to a Bayesian prior?

## Mini Exercise

Pick a small dataset. Derive the MLE for a Bernoulli model by hand and confirm it equals the sample mean.

## Diagram

```mermaid
flowchart LR
    M[Model p(x;θ)] --> L[Likelihood Π p(x_i;θ)]
    D[Data] --> L
    L --> LL[Log-likelihood]
    LL --> O[argmax θ]
    O --> P[θ_hat]
```

---
## Navigation

[⬅ Previous](05-bayes-theorem.md) | [🏠 Home](../README.md) | [➡ Next](07-hypothesis-testing.md)
