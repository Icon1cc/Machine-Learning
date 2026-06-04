# Statistics Mock

## Scenario

You are interviewing for a data or ML role with a statistics round. The prompt: "Our checkout
conversion rate dropped from 4.0 percent to 3.7 percent week over week. Leadership is alarmed. Is this
drop real, and how would you find out what caused it?"

## Round Format

A 60-minute round: 5 minutes clarifying the metric, 15 minutes on whether the drop is signal or
noise, 20 minutes on root-cause investigation, 10 minutes on the statistics, and 10 minutes on
communicating the finding.

## Interviewer Prompt

This is an applied statistics and diagnosis problem. Show that you can tell noise from signal, reason
about confounders, and structure an investigation without jumping to conclusions.

## Expected Clarification Questions

- How many sessions are behind each percentage (is 0.3 points even outside noise)?
- Did anything change: a release, a payment provider, a marketing source mix shift?
- Is the drop uniform, or concentrated in a segment (device, country, browser)?
- Is "conversion" defined the same way both weeks (no logging change)?
- Is there weekly seasonality that makes week-over-week the wrong comparison?

## Expected Answer or Design

A strong candidate first asks whether 4.0 to 3.7 is even statistically meaningful given the sample
size. With millions of sessions, a 0.3 point drop is likely real; with thousands, it could be noise.
Compute the difference in proportions, its standard error, and a confidence interval. If the interval
excludes zero, treat it as real and investigate.

Investigation is segment-first: slice conversion by device, browser, country, traffic source, and new
versus returning users. A drop concentrated in one segment (say, a specific browser after a release)
points to a bug, not a market change. Check for a logging or instrumentation change that redefined the
metric, a classic false alarm. Correlate the timing with deploys and incidents. Communicate clearly:
state whether the drop is statistically real, the most likely cause with evidence, the confidence
level, and the recommended action. Avoid claiming a cause without supporting segment evidence.

## Worked Strong Answer Outline

1. Is it real? Difference in proportions plus a confidence interval, given the sample size.
2. Rule out a metric-definition or logging change first.
3. Slice by segment; a concentrated drop implies a bug.
4. Correlate with deploys, incidents, and traffic-mix shifts.
5. Communicate: real or not, likely cause, confidence, recommended action.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Signal vs noise | Uses sample size and a confidence interval | Assumes the drop is real or fake |
| Confounders | Checks logging changes and seasonality | Ignores instrumentation and seasonality |
| Investigation | Segment-first, ties to deploys | Guesses a single cause immediately |
| Statistics | Difference in proportions, CI | Hand-waves significance |
| Communication | States confidence and action | Reports a number with no interpretation |

## Red Flags

- Declaring the drop real or fake without checking sample size.
- Ignoring a possible logging or metric-definition change.
- Jumping to one cause with no segment evidence.
- Comparing week-over-week despite known weekly seasonality.
- Presenting a conclusion with no confidence level.

## Follow-Up Questions

- The drop is entirely in one browser version. What is your hypothesis and next step?
- Sample size is small and the CI includes zero. What do you tell leadership?
- How would you set up an alert so you catch the next drop automatically?

## Self-Review Checklist

- Did I test whether the drop is statistically real?
- Did I rule out logging and metric-definition changes?
- Did I slice by segment before guessing a cause?
- Did I use a difference in proportions and a confidence interval?
- Did I communicate confidence and a recommended action?

---
## Navigation

[⬅ Previous](06-agent-system-design-mock.md) | [🏠 Home](../README.md) | [➡ Next](08-deep-learning-mock.md)
