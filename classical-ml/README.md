# Classical ML

## Folder Purpose

Supervised and unsupervised machine learning algorithms, evaluation, interpretability, and model selection.

## Beginner Intuition

Classical ML is the toolbox for structured (tabular) data: regression, trees, ensembles, clustering,
and dimensionality reduction. On most tabular problems these beat deep learning, train in seconds, and
are easier to explain. The skill is matching the model family to the data and the question.

## Why It Matters

A huge share of real business ML is still tabular: pricing, churn, fraud, risk, demand. Reaching for a
neural network on a 50k-row table is a classic anti-pattern. Knowing this toolbox makes you faster and
more credible, and gradient-boosted trees are the default strong baseline almost everywhere.

## Who Should Read This Section

Read this if you work with tabular data, prepare for ML-engineer or data-scientist interviews, or want
a strong baseline before considering deep learning. It pairs with the evaluation and feature
engineering material.

## Recommended Reading Order

Read in order: linear and logistic regression first, then distance and probabilistic models, then
trees and ensembles, then SVM, then clustering and PCA, then model selection, cross-validation,
metrics, and interpretability.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Linear Regression](01-linear-regression.md) |
| 2 | [Logistic Regression](02-logistic-regression.md) |
| 3 | [K Nearest Neighbors](03-k-nearest-neighbors.md) |
| 4 | [Naive Bayes](04-naive-bayes.md) |
| 5 | [Decision Trees](05-decision-trees.md) |
| 6 | [Random Forests](06-random-forests.md) |
| 7 | [Gradient Boosting](07-gradient-boosting.md) |
| 8 | [Xgboost Lightgbm Catboost](08-xgboost-lightgbm-catboost.md) |
| 9 | [Support Vector Machines](09-support-vector-machines.md) |
| 10 | [K Means Clustering](10-k-means-clustering.md) |
| 11 | [Hierarchical Clustering](11-hierarchical-clustering.md) |
| 12 | [DBSCAN](12-dbscan.md) |
| 13 | [PCA](13-pca.md) |
| 14 | [Anomaly Detection](14-anomaly-detection.md) |
| 15 | [Time Series Basics](15-time-series-basics.md) |
| 16 | [Model Selection](16-model-selection.md) |
| 17 | [Cross Validation](17-cross-validation.md) |
| 18 | [Evaluation Metrics](18-evaluation-metrics.md) |
| 19 | [Interpretability Shap Lime](19-interpretability-shap-lime.md) |
| 20 | [Classical ML Interview Patterns](20-classical-ml-interview-patterns.md) |

## Real-World Examples

- Fraud detection: logistic regression as a transparent baseline, then LightGBM for accuracy.
- Customer churn: gradient boosting on behavioral features, explained with SHAP for the retention
  team.
- Customer segmentation: K-Means or DBSCAN on usage features.
- Demand forecasting: time-series features fed into a boosted-tree regressor.

## Pattern Recognition

- "Tabular data, need accuracy" points to gradient boosting.
- "Need to explain the decision" points to linear models or SHAP on trees.
- "No labels, group similar items" points to clustering.
- "Too many correlated features" points to PCA or regularization.

## Common Mistakes

- Jumping to deep learning on small tabular data.
- Forgetting to scale features for KNN, SVM, and linear models (trees do not need it).
- Using accuracy on imbalanced data instead of PR-AUC or recall at a budget.
- Reading raw tree split counts as importance instead of SHAP or permutation importance.

## Interview Notes

Expect "random forest vs gradient boosting", "L1 vs L2", "why scale for SVM but not trees", "how do
you handle imbalance", "bagging vs boosting". Bagging reduces variance in parallel; boosting reduces
bias sequentially.

## What You Should Know After Finishing

- Which model family fits which data shape and constraint.
- The difference between bagging and boosting and when each helps.
- How to evaluate under imbalance and tune a decision threshold.
- How to interpret a model with coefficients, SHAP, or permutation importance.

## Suggested Exercises

- For a 100k-row, 10 percent-positive dataset, write your baseline-to-strong model progression.
- Explain why scaling matters for SVM but not for a decision tree.
- Choose a metric and threshold for a fraud model with a fixed review budget.
- Use SHAP on a small model and explain one prediction in plain language.

## Navigation

[🏠 Home](../README.md)
