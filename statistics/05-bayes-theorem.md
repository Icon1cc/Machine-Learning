# Bayes' Theorem

## Beginner-Friendly Intuition

Bayes' theorem updates a belief in light of evidence. You start with a prior probability of a hypothesis, observe evidence, and end with a posterior probability. The same machinery underlies medical tests, spam classifiers, and Bayesian inference.

## Formal Explanation

`P(H | E) = P(E | H) P(H) / P(E)`. The posterior is proportional to likelihood times prior. The denominator is a normalization. For multiple hypotheses, the posterior is a categorical distribution over them. Updating with new evidence `E2` (independent given `H`) just multiplies in another likelihood.

## Why It Matters in Real Jobs

Naive Bayes classifiers, Bayesian A/B tests, and many uncertainty estimates use Bayes' rule directly. Even non-Bayesian engineers should understand it for diagnostic problems: a positive medical test does not mean the disease is likely if the prior is small.

## How It Works Step by Step

1. Write the prior `P(H)` from base rates or domain knowledge.
2. Write the likelihood `P(E | H)` from data or model.
3. Multiply, normalize, and read the posterior.
4. Update with new evidence by multiplying in more likelihoods.
5. Communicate the result with both the posterior and the underlying assumptions.

## Real-World Example

A medical test has 99 percent sensitivity and 99 percent specificity for a disease that has 1 in 1000 prevalence. A positive result yields a posterior probability of disease around 9 percent, not 99 percent. Without applying Bayes, the test result is dangerously misinterpreted.

## Choosing a Prior

When the prior is not given, you have to pick one. Three common families:

- **Uninformative or weakly informative.** A uniform prior over a bounded parameter, or a wide Gaussian centered at zero. Useful when you genuinely have no domain knowledge or want the posterior to be data-driven.
- **Conjugate.** A prior chosen so the posterior stays in the same family. Beta prior + Bernoulli data gives a Beta posterior. Gaussian prior on the mean + Gaussian data gives a Gaussian posterior. Conjugate priors are popular because they have closed-form updates; they are still subjective choices.
- **Hierarchical.** When you have many related groups (e.g., conversion rates for many countries), put a prior on the group-level parameter and let the data partially pool across groups. This automatically regularizes small-sample groups toward the global average.

The biggest mistake is picking a flat prior to seem objective when domain knowledge exists. A flat prior on a probability that you know is rare will produce a posterior that is miscalibrated for small samples; a weakly informative prior centered on the realistic base rate is honest, not biased.

## Worked Example: Naive Bayes with Two Features

A classifier predicts spam vs ham given two binary features: contains the word "free" (`F`) and is sent at night (`N`). From training data:

- `P(spam) = 0.3`, `P(ham) = 0.7`.
- `P(F = 1 | spam) = 0.6`, `P(F = 1 | ham) = 0.1`.
- `P(N = 1 | spam) = 0.5`, `P(N = 1 | ham) = 0.2`.

A new email has `F = 1, N = 1`. Naive Bayes assumes the features are conditionally independent given the class:

- Numerator for spam: `P(spam) P(F | spam) P(N | spam) = 0.3 * 0.6 * 0.5 = 0.09`.
- Numerator for ham: `P(ham) P(F | ham) P(N | ham) = 0.7 * 0.1 * 0.2 = 0.014`.

Posterior `P(spam | F = 1, N = 1) = 0.09 / (0.09 + 0.014) ≈ 0.865`. The single positive evidence "contains 'free'" combined with "sent at night" pushes posterior spam probability from a 30 percent prior to nearly 87 percent. Naive Bayes is "naive" because the conditional independence assumption is rarely exactly true; in practice it works surprisingly well, especially in text where features are sparse.

## Common Mistakes

- Ignoring the prior when interpreting test results.
- Treating a posterior as a frequency (interpretation depends on Bayesian vs frequentist).
- Picking a flat prior when a real prior exists.
- Forgetting that likelihoods must integrate to 1 over evidence, not over hypotheses.

## Interview Angle

**Question:** Explain Bayes' theorem and apply it to a diagnostic test problem.

**Strong answer:** Posterior = likelihood times prior over evidence. Apply: with prevalence 0.001, sensitivity 0.99, specificity 0.99, the false-positive rate is 0.01 across 999 healthy people, producing about 10 false positives for every true positive. The posterior probability of disease given a positive test is roughly 9 percent.

**Weak answer:** Quote the formula without explaining how the prior changes the answer.

**Follow-up questions:**

- What is the difference between prior and posterior?
- How does naive Bayes use this rule?
- When would you use a Bayesian A/B test?
- How do you pick a prior when you do not have data?

## Mini Exercise

Pick a binary classification problem. Estimate base rate, sensitivity, and specificity from data. Compute the posterior probability of the positive class given a positive prediction.

## Diagram

```mermaid
flowchart LR
    Pr[Prior P(H)] --> Po[Posterior P(H|E)]
    L[Likelihood P(E|H)] --> Po
    Po --> D[Decision]
    E2[New evidence E2] --> Po
```

---
## Navigation

[⬅ Previous](04-expectation-variance-covariance.md) | [🏠 Home](../README.md) | [➡ Next](06-maximum-likelihood-estimation.md)
