# Diagrams

## Folder Purpose

Reusable Mermaid diagram source files that sketch the real flow of each major topic, from fundamentals
to deployment.

## Beginner Intuition

A good diagram compresses a whole topic into a flow you can redraw from memory. Each file here is a
small Mermaid source you can paste into any Markdown viewer to see the moving parts: how data flows,
where decisions branch, and where feedback loops close. They are study aids and interview
whiteboarding templates, not decoration.

## Why It Matters

In system-design interviews you will draw, not just talk. Being able to sketch the RAG pipeline, the
agent loop, or the MLOps lifecycle quickly signals real understanding. These diagrams give you a
correct mental template to reproduce under pressure.

## Who Should Read This Section

Use these whenever a lesson, case study, or interview needs a picture. They map one-to-one to the
topic folders, so reach for the matching diagram while studying that section.

## Recommended Reading Order

There is no fixed order. Open the diagram that matches the topic you are studying. Try to redraw it
from memory, then compare against the source.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [01-fundamentals.mmd](01-fundamentals.mmd) |
| 2 | [02-math.mmd](02-math.mmd) |
| 3 | [03-statistics.mmd](03-statistics.mmd) |
| 4 | [04-data-science.mmd](04-data-science.mmd) |
| 5 | [05-classical-ml.mmd](05-classical-ml.mmd) |
| 6 | [06-deep-learning.mmd](06-deep-learning.mmd) |
| 7 | [07-nlp.mmd](07-nlp.mmd) |
| 8 | [08-computer-vision.mmd](08-computer-vision.mmd) |
| 9 | [09-recommenders.mmd](09-recommenders.mmd) |
| 10 | [10-mlops.mmd](10-mlops.mmd) |
| 11 | [11-generative-ai.mmd](11-generative-ai.mmd) |
| 12 | [12-llms.mmd](12-llms.mmd) |
| 13 | [13-vector-databases.mmd](13-vector-databases.mmd) |
| 14 | [14-rag.mmd](14-rag.mmd) |
| 15 | [15-agents.mmd](15-agents.mmd) |
| 16 | [16-production-ai.mmd](16-production-ai.mmd) |
| 17 | [17-ethics-safety.mmd](17-ethics-safety.mmd) |
| 18 | [18-interviews.mmd](18-interviews.mmd) |
| 19 | [19-capstones.mmd](19-capstones.mmd) |
| 20 | [20-model-evaluation.mmd](20-model-evaluation.mmd) |
| 21 | [21-feature-engineering.mmd](21-feature-engineering.mmd) |
| 22 | [22-monitoring.mmd](22-monitoring.mmd) |
| 23 | [23-retrieval.mmd](23-retrieval.mmd) |
| 24 | [24-tool-use.mmd](24-tool-use.mmd) |
| 25 | [25-deployment.mmd](25-deployment.mmd) |

## Real-World Examples

- The RAG diagram mirrors how a production assistant retrieves, reranks, and grounds an answer.
- The agents diagram is the loop you would whiteboard for an agent design interview.
- The MLOps diagram is the lifecycle you would defend when asked "how do you keep a model healthy".

## Pattern Recognition

- Branches (decision diamonds) mark where most real-world failures happen.
- Feedback arrows mark where monitoring or retraining closes the loop.
- Two-stage flows (retrieve then rank, candidate then ranking) recur across retrieval and
  recommenders.

## What You Should Know After Finishing

- The canonical flow of each major topic, drawable from memory.
- Where the key decision points and feedback loops sit in each system.
- How the diagrams map onto the matching topic folders.

## Suggested Exercises

- Redraw the RAG and agent diagrams from memory, then check against the source.
- Annotate one diagram with the metric you would monitor at each stage.
- Extend the MLOps diagram with a rollback path and explain it out loud.

## Navigation

[🏠 Home](../README.md)
