# Data Science

## Folder Purpose

Practical data cleaning, exploration, feature engineering, visualization, experimentation, and communication.

## Beginner Intuition

Data science is the work between a vague business question and a defensible answer. Most of the job is
not modeling; it is cleaning messy data, exploring it until you understand it, engineering signals,
and communicating a result someone will act on. The model is often the smallest part.

## Why It Matters

Teams do not pay for accuracy; they pay for better decisions. A clean analysis with a clear
recommendation beats a fancy model nobody trusts. This section is where raw data becomes an
explanation a stakeholder can use.

## Who Should Read This Section

Read this if you are preparing for data-scientist or analyst roles, or if you build models but
struggle to frame the question, clean the data, or present the result. It connects directly to the
statistics section.

## Recommended Reading Order

Read in order: workflow first, then cleaning, exploration, feature engineering, missing and
imbalanced data, visualization, experimentation, business metrics, and communication last because it
ties everything together.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Data Science Workflow](01-data-science-workflow.md) |
| 2 | [Data Cleaning](02-data-cleaning.md) |
| 3 | [Exploratory Data Analysis](03-exploratory-data-analysis.md) |
| 4 | [Feature Engineering](04-feature-engineering.md) |
| 5 | [Handling Missing Values](05-handling-missing-values.md) |
| 6 | [Handling Imbalanced Data](06-handling-imbalanced-data.md) |
| 7 | [Data Visualization](07-data-visualization.md) |
| 8 | [Experimentation And Ab Testing](08-experimentation-and-ab-testing.md) |
| 9 | [Business Metrics](09-business-metrics.md) |
| 10 | [Communicating Results](10-communicating-results.md) |

## Real-World Examples

- A "revenue went up during the promo" claim that falls apart once you control for seasonality.
- A model that breaks because 30 percent of a key column was missing and silently imputed as zero.
- A dashboard that misleads because a bar chart started its axis at 90 instead of 0.
- A churn analysis that drives a retention campaign worth more than any model tweak.

## Pattern Recognition

- "The numbers look wrong" usually traces to data cleaning or a join that duplicated rows.
- "It works in the notebook" but not in the meeting means the communication failed, not the model.
- "We optimized the metric but the business did not improve" means the metric was a proxy, not the
  goal.
- A skewed or imbalanced target changes both modeling and metric choice.

## Common Mistakes

- Skipping exploration and trusting the data is clean.
- Imputing missing values without an indicator and without thinking about why they are missing.
- Optimizing a vanity metric instead of a decision metric.
- Presenting analysis without a clear recommendation.

## Interview Notes

Expect a case prompt like "metric X dropped, investigate" or "design an experiment for feature Y".
Strong answers clarify the decision, check the data, slice by segment, and end with a recommendation
and its risks.

## What You Should Know After Finishing

- The end-to-end workflow from question to communicated result.
- How to clean data and handle missing and imbalanced values responsibly.
- How to design and read an experiment.
- How to pick business metrics and present findings that drive action.

## Suggested Exercises

- Take a messy public dataset and write a five-step cleaning plan.
- Investigate a fictional metric drop: list checks in priority order.
- Turn one analysis into a three-sentence recommendation for a non-technical reader.
- Choose a decision metric and a guardrail metric for a product you use.

## Navigation

[🏠 Home](../README.md)
