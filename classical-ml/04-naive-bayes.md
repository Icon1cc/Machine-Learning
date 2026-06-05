# Naive Bayes

## Beginner-Friendly Intuition

Naive Bayes asks the simplest possible question: given that this email contains
the words "free", "viagra", and "click", what is the probability it is spam? It
applies Bayes' theorem to combine the prior probability of each class with the
likelihood of each feature, and pretends all features are independent given the
class. That independence assumption is almost always wrong, which is the "naive"
in the name. Yet Naive Bayes works astonishingly well on text and on small data
where every parameter you can avoid estimating is a parameter you do not need to
fit.

The intuition: when you have lots of features and not much data, a model that
ignores feature correlations and only estimates `P(feature | class)` for each
feature is robust because it has very few parameters. When the assumption breaks
mildly, it still ranks things correctly even if absolute probabilities are off.

## Formal Explanation

By Bayes' theorem, for a class `c` and feature vector `x = (x_1, ..., x_d)`:

```
P(c | x) ∝ P(c) · P(x | c) = P(c) · P(x_1, ..., x_d | c)
```

The naive assumption is that features are conditionally independent given the
class:

```
P(x | c) = Π_j P(x_j | c)
```

Predict the class that maximizes this product, equivalently the sum in log
space:

```
ĉ = argmax_c [ log P(c) + Σ_j log P(x_j | c) ]
```

Variants by feature distribution:

- **Multinomial NB.** Features are counts (word frequencies). Standard for text.
  Estimate `P(word | class)` from class-conditional word frequencies.
- **Bernoulli NB.** Features are binary (word present or absent). Useful when
  document length is uninformative.
- **Gaussian NB.** Features are continuous, modeled as Gaussians per class. Each
  class gets its own mean and variance per feature.
- **Categorical NB.** Discrete unordered categoricals.

**Laplace (additive) smoothing** prevents `P(word | class) = 0` from killing the
whole product when a word never appears in a class during training:

```
P(word_j | class) = (count_jc + α) / (Σ_j count_jc + α V)
```

with `α = 1` typical and `V` the vocabulary size.

**Always work in log space.** Multiplying many small probabilities underflows
floating point. Sum of log-probabilities is numerically stable.

## Why It Matters in Real Jobs

Naive Bayes is rarely the headline model in 2026, but it remains useful in three
roles. First, the spam-class baseline: text classification with TF-IDF +
Multinomial NB is competitive with logistic regression on small labeled sets and
trains in milliseconds. Second, the explanatory baseline before BERT or a
transformer: it tells you what fraction of the signal is "bag of words." If NB
gets 0.87 F1 and a fine-tuned transformer gets 0.91, the transformer's
contribution is small and may not justify the cost. Third, real-time scoring on
constrained devices: NB's inference is a sum of log-probabilities, microseconds
on any hardware.

It also has a teaching role: NB is the simplest concrete example of a
generative classifier, modeling `P(x | c)` rather than the discriminative
`P(c | x)` that logistic regression learns. That distinction matters in many
production decisions (handling unseen classes, rejection options, semi-supervised
learning).

## How It Works Step by Step

1. **Pick the variant by data type.** Counts -> Multinomial; binary indicators
   -> Bernoulli; continuous -> Gaussian; categorical -> Categorical.
2. **Compute class priors.** From training-set class frequencies, possibly
   uniform if you want to be robust to class imbalance.
3. **Compute conditional likelihoods.** Per-class word counts (Multinomial),
   per-class means and variances (Gaussian), etc.
4. **Apply Laplace smoothing.** Crucial; without it any unseen word in a class
   sets the joint to zero.
5. **Predict in log space.** `argmax_c [log prior + Σ log likelihood]`.
6. **Calibrate.** NB scores are not calibrated probabilities even when correct
   class is chosen. Apply isotonic regression or Platt scaling on a held-out
   set if you need probabilities.
7. **Validate against alternatives.** A logistic regression with the same
   features is the natural sanity check. If LR is meaningfully better, the
   independence assumption is too costly.

## Why It Surprisingly Wins on Text

Real text features are highly correlated ("free" and "money" co-occur). So why
does NB work? Two reasons. First, even when the absolute probabilities are
miscalibrated by the independence assumption, the **rankings** are often
correct: the class with higher product is still the right class. Second, with
small training sets and large vocabularies (say 10K words and 1K labeled
examples), there is not enough data to estimate joint distributions reliably.
Estimating `V` parameters per class (NB) instead of `V²` parameters (a model
that pairs words) can win by sample-efficiency alone. As data grows, logistic
regression and transformers overtake.

## Real-World Example

A team builds a triage classifier for support tickets, routing them to one of 8
queues. Training data is 4,200 labeled tickets. They tokenize, lowercase, drop
stopwords, and build TF-IDF vectors with the top 5,000 terms. Multinomial NB
with `α = 1` reaches macro F1 = 0.74. Logistic regression with L2 reaches 0.78.
A fine-tuned distilbert reaches 0.83 but takes 60 ms per inference vs 0.3 ms
for NB. The team ships NB as the fallback (when the GPU service is unavailable)
and as the explanation tool: per ticket, they show the top three words that
contributed to the decision (highest `log P(word | class)` minus mean across
classes). NB makes that interpretation trivial; the transformer does not.

## Common Mistakes

- Skipping Laplace smoothing and getting `-inf` probabilities for any unseen
  word.
- Multiplying probabilities directly instead of summing log-probabilities;
  underflow on long documents.
- Using Gaussian NB on heavily skewed continuous features without log
  transforming first.
- Treating NB scores as probabilities without calibration.
- Forgetting that the independence assumption rarely holds; do not use NB to
  estimate causal feature effects.
- Comparing NB to logistic regression on tiny data and concluding NB is
  outdated; on small data NB often matches or beats LR.
- Using one-hot encoded high-cardinality features with Multinomial NB; switch
  to Categorical or hash the feature.

## Interview Angle

**Question:** Why does Naive Bayes often beat logistic regression on small text
datasets even though the conditional independence assumption is wrong?

**Strong answer:** Two factors. First, with `V` features and `n << V` examples,
estimating `V` per-class likelihoods is statistically much more reliable than
fitting `V` interacting weights via gradient descent on cross-entropy. NB's
parameter count is independent of the number of feature interactions; LR's
optimal solution depends on those interactions. Second, NB minimizes a
generative criterion that has a higher asymptotic error than LR but lower
finite-sample variance (Ng and Jordan, 2001). So NB converges faster as `n`
grows, even though its final error is higher. The crossover happens around
`n / V ≈ 1`. For text in production this means NB is a strong baseline up to a
few thousand examples and gets overtaken by LR and then transformers as data
grows.

**Weak answer:** "Independence is fine for text" or "NB always works on text."

**Follow-up questions:**

- Derive the decision rule for binary Multinomial NB.
- When would you prefer Bernoulli NB to Multinomial NB?
- How does Laplace smoothing relate to Bayesian priors?
- What is the difference between a generative and a discriminative classifier?

## Mini Exercise

Take a small text classification dataset (20 newsgroups, IMDB sample). Fit
Multinomial NB with `α ∈ {0.01, 1, 10}`. Compare macro F1. Note how the optimal
`α` depends on dataset size.

## Diagram

```mermaid
flowchart LR
    X[Features x_1...x_d] --> L[Per-feature P(x_j | c) per class]
    L --> S[Sum log probs + log prior]
    S --> A[Argmax over classes]
    A --> P[Predicted class]
```

---
## Navigation

[⬅ Previous](03-k-nearest-neighbors.md) | [🏠 Home](../README.md) | [➡ Next](05-decision-trees.md)
