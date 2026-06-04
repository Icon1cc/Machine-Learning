# Statistics

## Folder Purpose

Probability, uncertainty, inference, testing, sampling, causality, and experimentation.

## Beginner Intuition

Statistics is how you reason from a sample to a conclusion while staying honest about uncertainty. You
never see the whole population, so you estimate, attach an interval, and ask whether a difference you
observed is real or could just be noise. This is the core skill behind every A/B test and metric
review.

## Why It Matters

Product decisions hinge on "is this change actually better". Without statistics you will ship changes
that do nothing, miss real wins, or fool yourself by peeking at experiments. Data science interviews
lean heavily on this section.

## Who Should Read This Section

Read this if you analyze experiments, interpret metric movements, or interview for data-science and
applied-scientist roles. It pairs tightly with the data-science experimentation lessons.

## Recommended Reading Order

Read in order: probability and random variables, then distributions and expectation, then Bayes and
MLE, then hypothesis testing and confidence intervals, then causation, A/B testing, and bias.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Probability Basics](01-probability-basics.md) |
| 2 | [Random Variables](02-random-variables.md) |
| 3 | [Common Distributions](03-common-distributions.md) |
| 4 | [Expectation Variance Covariance](04-expectation-variance-covariance.md) |
| 5 | [Bayes Theorem](05-bayes-theorem.md) |
| 6 | [Maximum Likelihood Estimation](06-maximum-likelihood-estimation.md) |
| 7 | [Hypothesis Testing](07-hypothesis-testing.md) |
| 8 | [Confidence Intervals](08-confidence-intervals.md) |
| 9 | [Correlation Vs Causation](09-correlation-vs-causation.md) |
| 10 | [Ab Testing](10-ab-testing.md) |
| 11 | [Sampling Bias And Data Leakage](11-sampling-bias-and-data-leakage.md) |
| 12 | [Statistics For Interviews](12-statistics-for-interviews.md) |

## Real-World Examples

- An A/B test shows 12.0 vs 11.5 percent conversion; a confidence interval tells you whether to ship.
- A "conversion dropped 0.3 points" alarm is noise on small samples and real on large ones.
- A model trained on a biased sample silently fails on the underrepresented group.
- Bayes powers spam filters and medical-test reasoning (base rates matter).

## Pattern Recognition

- "Is this difference real" points to a hypothesis test and a confidence interval.
- "We stopped the test when it looked good" points to peeking and inflated false positives.
- "X correlates with Y" should trigger a confounder hunt before any causal claim.
- "The metric moved" should trigger a check for a logging or definition change first.

## Common Mistakes

- Saying the p-value is the probability the hypothesis is true.
- Confusing statistical significance with practical (effect-size) significance.
- Peeking at experiments and stopping early.
- Ignoring multiple-comparison inflation across many metrics.

## Interview Notes

Expect "explain a p-value to a PM", "Type I vs Type II error", "how would you size an A/B test",
"correlation vs causation". Always tie the statistic to the decision it supports.

## What You Should Know After Finishing

- How to turn a sample into an estimate with a confidence interval.
- How a hypothesis test works and what a p-value does and does not mean.
- How to design an A/B test and avoid peeking and bias.
- When correlation can and cannot support a causal claim.

## Suggested Exercises

- Design an A/B test for a checkout change: metric, null, MDE, guardrail, and anti-peeking plan.
- Explain a p-value to a non-technical stakeholder in two sentences.
- Given a 0.3 point metric drop, decide what sample size would make it meaningful.
- List three confounders for "users who get feature X spend more".

## Navigation

[🏠 Home](../README.md)
