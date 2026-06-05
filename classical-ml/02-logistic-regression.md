# Logistic Regression

## Beginner-Friendly Intuition

Logistic regression is linear regression's cousin for classification. Instead of
predicting a number, it predicts a probability. It does this by computing a
linear score from the features and then squashing the score through a sigmoid so
the output sits between 0 and 1. The decision boundary is still linear; only
the output is bounded.

The reason teams keep reaching for logistic regression is simple: it is a
probability model. The output is a calibrated chance, not a raw score, which is
exactly what every downstream system (pricing, thresholding, expected-value
math) wants. It is also fast, interpretable per-feature in log-odds space, and
hard to break.

## Formal Explanation

For a binary target `y ∈ {0, 1}`, logistic regression models

```
P(y = 1 | x) = σ(w^T x + b)    where σ(z) = 1 / (1 + e^{-z})
```

Equivalently, the **log-odds** are linear in `x`: `log(p / (1 - p)) = w^T x + b`.
A coefficient `w_j` says "a one-unit increase in feature `j` adds `w_j` to the
log-odds." Exponentiating gives the **odds ratio** `e^{w_j}`.

Training maximizes the log-likelihood, which equals minimizing binary
cross-entropy:

```
L(w) = - Σ_i [ y_i log p_i + (1 - y_i) log (1 - p_i) ]
```

There is no closed form because of the sigmoid; solvers use Newton-Raphson
(IRLS), L-BFGS, or SGD. The loss is convex, so any local minimum is global.

Multiclass extensions:

- **One-vs-rest (OvR).** Train K binary classifiers, one per class. Simple but
  produces uncalibrated, non-summing-to-one scores.
- **Softmax (multinomial logistic regression).** Replace the sigmoid with a
  softmax over K class-specific scores. Outputs are a proper distribution.

Regularization:

- **L2 (ridge):** add `λ ||w||²`. Shrinks coefficients smoothly, stabilizes
  collinear features.
- **L1 (lasso):** add `λ ||w||₁`. Drives weights to exact zero, doing feature
  selection.
- **Elastic net:** convex combination of L1 and L2.

## Why It Matters in Real Jobs

Logistic regression is the workhorse classifier of regulated industries (credit,
insurance, healthcare, fraud) and the first model anyone with a serious tabular
classification problem builds. Three production reasons. First, calibrated
probabilities: a logistic regression scored 0.7 actually corresponds to roughly
70 percent positive frequency once features are reasonable. Tree models almost
never give you that without post-hoc Platt scaling. Second, monotonicity and
auditability: a regulator can ask "why did this customer get rejected?" and you
can answer by listing coefficients and feature values. Third, latency: scoring is
a dot product, microseconds even at scale.

When does it lose? When the relationship between features and log-odds is
genuinely non-linear and you do not engineer interactions or splines by hand. In
those cases, GBMs typically gain 1 to 5 AUC points.

## How It Works Step by Step

1. **Frame the binary target precisely.** What does `y = 1` mean, and at what
   moment is it observed? Hidden temporal structure is the most common bug.
2. **Profile features.** Standardize numerics. One-hot or target-encode
   categoricals. Add interaction terms or splines if you suspect non-linearity.
3. **Pick regularization.** L2 by default; L1 or elastic net if you want
   sparsity for interpretability or compute.
4. **Fit.** Use `sklearn.linear_model.LogisticRegression` for small data,
   `SGDClassifier(loss='log_loss')` for very large data.
5. **Tune the threshold.** The default 0.5 is rarely optimal. Choose the
   threshold from the precision-recall trade-off your business cares about.
6. **Calibrate if needed.** Logistic regression is naturally well-calibrated
   under correct specification, but heavy regularization, class weighting, or
   resampling can shift scores. Check with a reliability diagram; apply Platt
   scaling or isotonic regression if needed.
7. **Report metrics with uncertainty.** AUC and PR-AUC with bootstrap CIs;
   per-segment metric for the populations the business cares about.

## Real-World Example

A bank builds a churn classifier. Their first logistic regression with 23
features gets ROC-AUC 0.82, PR-AUC 0.41 (positive class is 8 percent), and a
calibration error of 0.013. They tune L2 from `C = 1.0` to `C = 0.1` (more
regularization) via 5-fold CV; AUC drops to 0.81 but per-segment AUC tightens.
They tune the decision threshold to 0.18 to hit 80 percent precision; recall is
0.36. The product team uses the score directly in a retention campaign sized to
the top decile by predicted probability. Six months later, a gradient boosted
model lifts AUC to 0.86, but the team keeps logistic regression as the
explainability artifact: when a customer asks "why was I in the campaign?", the
top three coefficients answer.

## Common Mistakes

- Using accuracy on imbalanced data; predicting "no" always can score above 95
  percent and is useless.
- Treating odds ratios as risk ratios. They differ when the base rate is not
  small.
- Forgetting to one-hot encode unordered categoricals; integer encoding implies
  an ordering that does not exist.
- Standardizing test data with test statistics rather than train.
- Using OvR when you actually want a probability distribution; use softmax.
- Tuning the threshold on the test set instead of validation.
- Comparing AUC across datasets with different positive rates and concluding one
  model is better; PR-AUC is more honest under imbalance.

## Interview Angle

**Question:** Why is logistic regression a probability model and linear
regression on a 0/1 target is not?

**Strong answer:** Linear regression on a 0/1 target produces predictions that
can fall outside `[0, 1]`, has constant residual variance assumptions that
classification violates, and gives no log-likelihood interpretation. Logistic
regression's sigmoid maps any real-valued linear combination into a valid
probability, and the cross-entropy loss is the negative log-likelihood under a
Bernoulli model. So the output is calibrated by construction (when the model is
correctly specified), and you can plug it into expected-value calculations.
Linear regression's output cannot.

**Weak answer:** Saying linear regression "does not work" without explaining
why, or claiming logistic regression is just linear regression with a different
loss.

**Follow-up questions:**

- Derive the gradient of the log-loss with respect to `w`.
- When would you pick L1 over L2?
- How does class imbalance affect the coefficients?
- What is the difference between a probability and a risk?

## Mini Exercise

Take any binary tabular dataset. Fit a logistic regression with `C = 1.0`. Plot
the reliability diagram (predicted probability vs actual frequency, in deciles).
If it is uncalibrated, fit isotonic regression on a held-out fold and replot.

## Diagram

```mermaid
flowchart LR
    X[Features x] --> Z[Linear score w·x + b]
    Z --> S[Sigmoid σ(z)]
    S --> P[Probability p]
    P --> T[Threshold]
    T --> D[Decision]
```

---
## Navigation

[⬅ Previous](01-linear-regression.md) | [🏠 Home](../README.md) | [➡ Next](03-k-nearest-neighbors.md)
