# Probability Basics

## Beginner-Friendly Intuition

Probability is the language for reasoning about uncertainty. Every ML prediction is a guess; probability tells you how to attach a confidence to it, how to combine evidence, and how often you should be right in the long run.

## Formal Explanation

A sample space `Ω` lists all possible outcomes. An event is a subset of `Ω`. A probability assigns each event a number in `[0,1]` such that `P(Ω) = 1` and disjoint events add. Joint probability `P(A,B)`, conditional `P(A|B) = P(A,B)/P(B)`, and independence (`P(A,B)=P(A)P(B)`) are the building blocks. The chain rule `P(x_1,...,x_n) = Π P(x_i | x_<i)` is the foundation of language models and many graphical models.

## Why It Matters in Real Jobs

Classifiers output probabilities; calibration says whether those probabilities match observed frequencies. Bayesian reasoning combines prior belief with evidence. A/B tests use probability to decide whether a difference is real. Retrieval and recommenders rank by probability of relevance.

## How It Works Step by Step

1. Define the sample space and the event of interest.
2. Write the probabilities of the simple events from data or assumption.
3. Combine using the rules: complement, sum (disjoint), product (independent), conditional.
4. Sanity-check: do probabilities sum to 1? Are conditionals between 0 and 1?
5. Translate the answer back into a decision (accept, reject, route to review).

## Real-World Example

A spam filter outputs `P(spam | message) = 0.92`. The product rule and prior data say a 0.92 model probability corresponds to actual spam in 88 percent of cases (the model is slightly overconfident). Calibration analysis catches this; uncalibrated probabilities make downstream thresholds wrong.

## Numeric Chain Rule and Independence

Chain rule with two events. Suppose 30 percent of users sign up (`P(S) = 0.3`), and among those who sign up, 40 percent activate within a week (`P(A | S) = 0.4`). The joint probability of both is `P(A, S) = P(S) P(A | S) = 0.3 * 0.4 = 0.12`. So 12 percent of all users sign up and activate. Add a third event: among activators, 60 percent are still around at 30 days (`P(R | A, S) = 0.6`). The full chain gives `P(R, A, S) = 0.3 * 0.4 * 0.6 = 0.072`, or 7.2 percent retained at 30 days. This is exactly the structure language models use: `P(token_3 | token_1, token_2) * P(token_2 | token_1) * P(token_1)`.

When independence is violated. Suppose two app screens are clicked by 20 percent of users each, but the same engaged users tend to click both. If clicks were independent, the joint click rate would be `0.2 * 0.2 = 0.04`. If you measure the actual joint rate at 0.12, the events are positively correlated; treating them as independent in a feature engineering pipeline (e.g., logging `click_a_and_b = click_a * click_b` and modeling each separately as a probability) systematically underestimates the joint event by a factor of 3. The fix: model the conditional `P(B | A)` directly or use joint counts.

## Common Mistakes

- Confusing `P(A|B)` with `P(B|A)` (the prosecutor's fallacy).
- Assuming independence when events are correlated.
- Using model output as a probability without calibrating.
- Treating a low-probability event as impossible after observing it once.

## Interview Angle

**Question:** Explain conditional probability, the chain rule, and how language models use them.

**Strong answer:** `P(A|B)` is the probability of `A` given `B` happened, equal to `P(A,B)/P(B)`. The chain rule decomposes a joint distribution into a product of conditionals: `P(x_1, x_2, x_3) = P(x_1) P(x_2|x_1) P(x_3|x_1, x_2)`. Language models predict the next token conditional on the previous ones, training to maximize the chain-rule likelihood of training text.

**Weak answer:** Confuse joint and conditional, or claim language models predict joint distributions directly.

**Follow-up questions:**

- Why are calibrated probabilities important for thresholding?
- What does `P(B) = 0` imply for `P(A|B)`?
- How would you check independence between two features?
- What is the difference between marginal and joint probabilities?

## Mini Exercise

Take any classifier you have used. Bin its predicted probabilities into deciles and plot empirical accuracy per bin. Note where the model is overconfident or underconfident.

## Diagram

```mermaid
flowchart LR
    Ev[Evidence E] --> C[P(H | E)]
    H[Hypothesis H] --> Pr[Prior P(H)]
    Pr --> C
    Ev --> L[Likelihood P(E | H)]
    L --> C
```

---
## Navigation

[⬅ Previous](../math/12-distance-metrics.md) | [🏠 Home](../README.md) | [➡ Next](02-random-variables.md)
