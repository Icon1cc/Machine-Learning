# Interview Prep

## Folder Purpose

Role-specific roadmaps, technical question sets, behavioral preparation, resume positioning, and
final revision drills for AI, ML, LLM, data science, and system design interviews. This folder is
the place to turn broad study into timed answers that can survive follow-up questions.

## Who Should Read This Section

Use this section when you already know the concepts but need sharper interview execution. It is for
learners who can read a lesson and understand it, but still need practice turning that knowledge into
clear answers with assumptions, baselines, metrics, failure modes, and production tradeoffs.

Read it especially if you are preparing for:

- AI Engineer or GenAI Engineer interviews focused on LLM apps, RAG, tools, and product judgment.
- Machine Learning Engineer interviews focused on data pipelines, training, serving, monitoring, and
  model quality.
- Data Scientist interviews focused on statistics, experimentation, business metrics, and
  communication.
- Big-tech loops where one answer may be stretched into coding, ML design, product sense, and
  behavioral follow-ups.

## Recommended Reading Order

Start with the roadmap for the role you want, then jump to the question files that match your
weakest round. Do not read this folder passively. For every file, answer before reading the strong
answer, compare against the weak answer, then rewrite your response in your own words.

Suggested paths:

- **AI Engineer path:** 01, 03, 09, 10, 11, 12, 13, 14, 15.
- **ML Engineer path:** 02, 05, 06, 07, 08, 12, 13, 14, 15.
- **Data Scientist path:** 04, 05, 06, 07, 12, 13, 14, 15.
- **Final-week path:** 05 through 13, then 15 twice under a timer.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [AI Engineer Roadmap](01-ai-engineer-roadmap.md) |
| 2 | [ML Engineer Roadmap](02-ml-engineer-roadmap.md) |
| 3 | [LLM Engineer Roadmap](03-llm-engineer-roadmap.md) |
| 4 | [Data Scientist Roadmap](04-data-scientist-roadmap.md) |
| 5 | [Common ML Interview Questions](05-common-ml-interview-questions.md) |
| 6 | [Statistics Interview Questions](06-statistics-interview-questions.md) |
| 7 | [Classical ML Interview Questions](07-classical-ml-interview-questions.md) |
| 8 | [Deep Learning Interview Questions](08-deep-learning-interview-questions.md) |
| 9 | [LLM Interview Questions](09-llm-interview-questions.md) |
| 10 | [RAG Interview Questions](10-rag-interview-questions.md) |
| 11 | [Agent Interview Questions](11-agent-interview-questions.md) |
| 12 | [ML System Design Interview Questions](12-ml-system-design-interview-questions.md) |
| 13 | [Behavioral AI Interviews](13-behavioral-ai-interviews.md) |
| 14 | [Resume Project Strategy](14-resume-project-strategy.md) |
| 15 | [Final Revision Checklist](15-final-revision-checklist.md) |

## What You Should Know After Finishing

- How to open an ambiguous prompt by clarifying user, decision, data, constraints, and success
  metric.
- How to defend a baseline before proposing a more complex model, RAG system, or agent.
- How to explain tradeoffs across quality, latency, cost, privacy, safety, maintainability, and user
  trust.
- How to turn a project into an interview story with problem framing, measurable impact, technical
  depth, and honest limitations.
- How to recover from follow-up pressure without changing assumptions silently.

## Answer Quality Bar

A strong answer should name the product decision, the available signal, the simplest useful
baseline, the primary metric, the guardrail metrics, the most expensive failure mode, and the
production control that catches that failure. A weak answer usually names an impressive model first,
skips data quality, treats one offline metric as proof, or ignores monitoring and rollback.

Use this checklist after each practice answer:

- Did I clarify the user and decision before choosing the model?
- Did I explain why the baseline is not enough?
- Did I separate offline evaluation from production monitoring?
- Did I mention data leakage, drift, privacy, fairness, or safety when relevant?
- Did I state what I would do if the system fails after launch?

## Suggested Exercises

- Record a three-minute answer for one question, then rewrite it as six bullets: clarify, baseline,
  data, metric, failure mode, production plan.
- Take one file from `case-studies/` and turn it into a system design answer with requirements,
  architecture, evaluation, and rollback.
- Pick one project from `capstone-projects/` and write a resume bullet, a technical deep dive, and a
  failure-analysis story.
- Run a mock from `mocks/`, score yourself against the rubric, then return to the weakest question
  file in this folder.
- Before an interview, review `15-final-revision-checklist.md` and remove any answer that relies on
  memorized wording rather than concrete reasoning.

## Navigation

[🏠 Home](../README.md)
