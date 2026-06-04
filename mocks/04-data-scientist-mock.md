# Data Scientist Mock

## Scenario

You are interviewing for a Data Scientist role. The prompt: "Marketing ran a 10 percent discount for
two weeks. Revenue went up 6 percent during the promo. They want to make the discount permanent. Is
that a good decision? How would you actually know?"

## Round Format

A 60-minute round: 5 minutes clarifying the business question, 15 minutes on why the naive comparison
is flawed, 20 minutes on designing a clean experiment, 10 minutes on metrics and statistics, and 10
minutes on the recommendation and its risks.

## Interviewer Prompt

This is a causal-inference and experimentation problem. The interviewer wants to see whether you can
resist a tempting but wrong conclusion and design something that actually measures causal impact.

## Expected Clarification Questions

- What is the real objective: revenue, profit margin, or long-term customer value?
- Was the discount given to everyone at once, or could we randomize?
- What else happened in those two weeks (seasonality, a holiday, another campaign)?
- Does the discount pull forward future purchases rather than create new ones?
- What is the cost of the discount, so we can judge margin, not just revenue?

## Expected Answer or Design

A strong candidate immediately flags that "revenue went up 6 percent during the promo" is not causal
evidence. Confounders abound: seasonality, other campaigns, and purchase pull-forward. The clean
approach is a randomized experiment: split comparable customers into treatment (discount) and control
(no discount), run long enough to capture repeat behavior, and compare. If randomization is
impossible, use a difference-in-differences or a matched control region.

Metrics: the primary metric should be profit or margin-adjusted revenue, not gross revenue, because a
discount can raise revenue while destroying margin. Guardrails: long-term retention and purchase
frequency after the promo ends, to catch pull-forward. Statistics: pre-compute the sample size for a
minimum detectable effect, set alpha, avoid peeking, and report a confidence interval on the lift,
not just a point estimate. The recommendation is conditional: make it permanent only if the
margin-adjusted lift is positive and stable beyond the promo window.

## Worked Strong Answer Outline

1. Reject the naive before/during comparison; name the confounders.
2. Randomized A/B is the gold standard; diff-in-diff if not.
3. Optimize margin, not gross revenue.
4. Guardrail on post-promo retention to catch pull-forward.
5. Report a confidence interval and decide on stable, margin-positive lift.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Causal reasoning | Names confounders, demands randomization | Accepts the 6 percent as causal |
| Metric choice | Margin and long-term value, not gross revenue | Optimizes gross revenue |
| Experiment design | Sizing, control, no peeking | Vague "run a test" |
| Statistics | Confidence interval, effect size, power | Reports only a point estimate |
| Recommendation | Conditional and risk-aware | Unconditional "yes, make it permanent" |

## Red Flags

- Accepting the during-promo revenue bump as proof.
- Optimizing revenue while ignoring margin.
- Ignoring purchase pull-forward and post-promo behavior.
- Peeking at the test and stopping early.
- No confidence interval or sample-size reasoning.

## Follow-Up Questions

- You cannot randomize because legal requires the same price for everyone. Now what?
- The lift is significant but the confidence interval is wide. What do you tell marketing?
- How would you detect that the discount just pulled forward December sales into November?

## Self-Review Checklist

- Did I reject the naive causal claim and name confounders?
- Did I design a randomized or quasi-experimental test?
- Did I choose margin and long-term metrics over gross revenue?
- Did I reason about sample size, peeking, and confidence intervals?
- Did I give a conditional, risk-aware recommendation?

---
## Navigation

[⬅ Previous](03-llm-engineer-mock.md) | [🏠 Home](../README.md) | [➡ Next](05-rag-system-design-mock.md)
