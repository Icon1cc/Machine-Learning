# Fundamentals

## Folder Purpose

Core machine learning vocabulary, workflows, data splits, generalization, and model evaluation habits.

## Beginner Intuition

Machine learning is pattern-finding from examples instead of hand-written rules. You show a model
labeled data, it adjusts internal numbers to reduce error, and you check whether what it learned
holds on data it has never seen. Almost everything in this folder is a tool for answering one
question: will this model work on tomorrow's data, not just yesterday's?

## Why It Matters

Most real-world ML failures are fundamentals failures, not algorithm failures. A leaked feature, a
broken train/test split, or a metric that does not match the business goal sinks more projects than a
suboptimal model. Get these habits right and the rest of the curriculum builds cleanly on top.

## Who Should Read This Section

Start here if you are new to ML, or if you can train models but have been burned by a model that
looked great offline and failed in production. These are the concepts interviewers assume you have
internalized before they ask anything harder.

## Recommended Reading Order

Read in order. The arc goes from "what is ML" to data splits, to the bias-variance tradeoff, to the
full end-to-end workflow. Do not skip the splits and generalization lessons; they prevent the most
expensive mistakes.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is Machine Learning](01-what-is-machine-learning.md) |
| 2 | [AI Vs ML Vs Deep Learning Vs Data Science](02-ai-vs-ml-vs-deep-learning-vs-data-science.md) |
| 3 | [Supervised Unsupervised Self Supervised Reinforcement Learning](03-supervised-unsupervised-self-supervised-reinforcement-learning.md) |
| 4 | [Training Validation Test Splits](04-training-validation-test-splits.md) |
| 5 | [Overfitting Underfitting Bias Variance](05-overfitting-underfitting-bias-variance.md) |
| 6 | [Features Labels Datasets](06-features-labels-datasets.md) |
| 7 | [Models Parameters Hyperparameters](07-models-parameters-hyperparameters.md) |
| 8 | [Loss Functions And Optimization](08-loss-functions-and-optimization.md) |
| 9 | [Generalization](09-generalization.md) |
| 10 | [End-to-End ML Workflow](10-end-to-end-ml-workflow.md) |

## Real-World Examples

- A churn model scores 95 percent accuracy, but 95 percent of users do not churn, so it learned
  nothing useful. Fundamentals (baseline, metric choice) catch this immediately.
- A fraud model hits 0.98 AUC offline and 0.62 live because a feature leaked future information.
- A recommender overfits to last month's trends and degrades as tastes shift, which is a
  generalization problem.

## Pattern Recognition

- "Great offline, bad in production" usually means leakage or distribution shift.
- "Train accuracy high, validation low" means overfitting (high variance).
- "Both train and validation poor" means underfitting (high bias).
- "Accuracy looks amazing on rare events" means the metric is wrong for the imbalance.

## Common Mistakes

- Tuning on the test set, so the final number is optimistic.
- Choosing accuracy on imbalanced data.
- Comparing a model to nothing instead of to a baseline.
- Confusing parameters (learned) with hyperparameters (set by you).

## Interview Notes

Expect "explain bias-variance", "how do you split data and why", "what is overfitting and how do you
detect it", "why not just use accuracy". Strong answers always anchor to a baseline and a metric that
matches the cost of errors.

## What You Should Know After Finishing

- The difference between supervised, unsupervised, self-supervised, and reinforcement learning.
- How to split data cleanly and why the test set is touched only once.
- How to read loss curves to tell underfitting from overfitting.
- How to pick a metric and a baseline that match the real decision.

## Suggested Exercises

- Take a dataset and write its task type, baseline, primary metric, and one leakage risk.
- Sketch the train/validation/test split and explain what each set is allowed to influence.
- Draw the bias-variance curve and mark where overfitting and underfitting live.
- Explain to a non-technical friend why 95 percent accuracy can be useless.

## Navigation

[🏠 Home](../README.md)
