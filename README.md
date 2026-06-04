# Machine Learning

This repository is a personal learning path for machine learning, AI engineering, LLM systems, RAG,
agents, production AI, and interview preparation. It is designed as a practical engineering knowledge
base with lessons, case studies, quizzes, cheatsheets, mocks, notebooks, and runnable examples.

## Purpose

The purpose of this repository is to make machine learning study concrete. It connects concepts to
examples, interview prompts, diagrams, exercises, case studies, and portfolio projects so each topic
can be reviewed, practiced, and explained clearly.

## Who This Repository Is For

- Software engineers moving into AI or machine learning engineering.
- Data scientists who want stronger production and system design foundations.
- Students who want a clear path from fundamentals to applied projects.
- Practitioners preparing for AI Engineer, Machine Learning Engineer, LLM Engineer, Data Scientist,
  Applied Scientist, or GenAI Engineer interviews.

## Start Here

Start with [What Is Machine Learning?](fundamentals/01-what-is-machine-learning.md). Then read the
numbered files in each folder according to the recommended order below. Each learning file includes
intuition, formal explanation where useful, real-world relevance, common mistakes, interview angles,
an exercise, a Mermaid diagram, and navigation links.

## Beginner Path

1. Read `fundamentals/`, `math/`, and `statistics/`.
2. Run the first three notebooks in `notebooks/`.
3. Complete the fundamentals, linear algebra, and statistics quizzes.
4. Build one small baseline model from `src/ml_from_scratch/`.

## Deep Study Path

Use the full curriculum order from fundamentals through production AI. Take notes on assumptions,
metrics, failure modes, and deployment concerns after each folder. Pair every conceptual section with
one quiz, one cheatsheet review, and one small implementation or case study.

## Interview Preparation Path

Use [interview-prep/README.md](interview-prep/README.md) after completing the core technical
sections. Practice explaining tradeoffs out loud, then use [mocks/README.md](mocks/README.md) for
full-round simulation and scoring.

## Project and Case Study Path

Use [case-studies/README.md](case-studies/README.md) to learn how systems are framed and reviewed.
Use [capstone-projects/README.md](capstone-projects/README.md) to turn that knowledge into portfolio
projects with evaluation, failure analysis, and interview explanation.

## Learning Roadmap

```mermaid
flowchart LR
    Basics --> Math --> Statistics --> Python_and_Data[Python and Data]
    Python_and_Data --> Classical_ML[Classical ML] --> Deep_Learning[Deep Learning]
    Deep_Learning --> NLP --> Computer_Vision[Computer Vision] --> Recommenders
    Recommenders --> MLOps --> GenAI --> LLMs
    LLMs --> Vector_Databases[Vector Databases] --> RAG --> Agents
    Agents --> Production_AI[Production AI] --> ML_System_Design[ML System Design]
    ML_System_Design --> Ethics --> Case_Studies[Case Studies] --> Interviews --> Projects
```

## Table of Contents

| Section | What It Contains |
| --- | --- |
| [Fundamentals](fundamentals/README.md) | Core machine learning vocabulary, workflows, data splits, generalization, and model evaluation habits. |
| [Math](math/README.md) | Linear algebra, calculus, optimization, distance metrics, and information theory for machine learning. |
| [Statistics](statistics/README.md) | Probability, uncertainty, inference, testing, sampling, causality, and experimentation. |
| [Data Science](data-science/README.md) | Practical data cleaning, exploration, feature engineering, visualization, experimentation, and communication. |
| [Classical ML](classical-ml/README.md) | Supervised and unsupervised machine learning algorithms, evaluation, interpretability, and model selection. |
| [Deep Learning](deep-learning/README.md) | Neural networks, optimization, regularization, convolution, sequence models, attention, and transformers. |
| [NLP](nlp/README.md) | Text preprocessing, tokenization, embeddings, sequence modeling, transformers, semantic search, and NLP evaluation. |
| [Computer Vision](computer-vision/README.md) | Image tensors, convolution, classification, detection, segmentation, vision transformers, and multimodal models. |
| [Recommender Systems](recommender-systems/README.md) | Candidate generation, ranking, collaborative filtering, matrix factorization, and recommender evaluation. |
| [MLOps](mlops/README.md) | Reproducibility, experiment tracking, model registries, serving, monitoring, CI/CD, and governance. |
| [Generative AI](generative-ai/README.md) | Autoregressive models, VAEs, GANs, diffusion, multimodal generation, and generative AI evaluation. |
| [LLMs](llms/README.md) | Transformer decoder architecture, pretraining, instruction tuning, prompting, tools, evaluation, and serving. |
| [Vector Databases](vector-databases/README.md) | Embeddings, similarity search, ANN indexes, filtering, hybrid search, reranking, and vector search scaling. |
| [RAG](rag/README.md) | Document ingestion, chunking, embeddings, retrieval, reranking, generation, evaluation, observability, and security. |
| [Agents](agents/README.md) | Agent loops, tool use, planning, memory, multi-agent design, evaluation, observability, and risk controls. |
| [Production AI](production-ai/README.md) | Architecture patterns, latency, cost, caching, routing, fallbacks, privacy, monitoring, and product metrics. |
| [Machine Learning System Design](machine-learning-system-design/README.md) | System design practice for ML platforms, recommendation systems, search ranking, RAG, agents, evaluation, and real-time inference. |
| [Ethics Safety](ethics-safety/README.md) | Fairness, privacy, security risks, misuse, responsible AI, and governance. |
| [Case Studies](case-studies/README.md) | Applied ML and AI system case studies with production tradeoffs and interview discussion points. |
| [Interview Prep](interview-prep/README.md) | Role-specific roadmaps, technical question sets, behavioral preparation, and final revision checklists. |
| [Mocks](mocks/README.md) | Mock interview rounds with prompts, expected answers, scoring rubrics, and self-review material. |
| [Quizzes](quizzes/README.md) | Ten-question review sets with answer keys and explanations for retrieval practice. |
| [Cheatsheets](cheatsheets/README.md) | Compact reference pages for fast revision before projects and interviews. |
| [Capstone Projects](capstone-projects/README.md) | Project guides for portfolio work, implementation planning, evaluation, and interview explanation. |
| [Notebooks](notebooks/README.md) | Hands-on starter notebooks for NumPy, pandas, classical ML, neural networks, transformers, embeddings, and RAG. |
| [Source Examples](src/README.md) | Runnable educational Python examples for ML from scratch, RAG, agents, and simple serving. |
| [Diagrams](diagrams/README.md) | Reusable Mermaid diagram source files for learning paths and architecture sketches. |
| [Tools](tools/README.md) | Repository maintenance scripts for indexing, link validation, and Markdown quality checks. |

## Recommended Reading Order

[Fundamentals](fundamentals/README.md) -> [Math](math/README.md) -> [Statistics](statistics/README.md) -> [Data Science](data-science/README.md) -> [Classical ML](classical-ml/README.md) -> [Deep Learning](deep-learning/README.md) -> [NLP](nlp/README.md) -> [Computer Vision](computer-vision/README.md) -> [Recommender Systems](recommender-systems/README.md) -> [MLOps](mlops/README.md) -> [Generative AI](generative-ai/README.md) -> [LLMs](llms/README.md) -> [Vector Databases](vector-databases/README.md) -> [RAG](rag/README.md) -> [Agents](agents/README.md) -> [Production AI](production-ai/README.md) -> [Machine Learning System Design](machine-learning-system-design/README.md) -> [Ethics Safety](ethics-safety/README.md) -> [Case Studies](case-studies/README.md) -> [Interview Prep](interview-prep/README.md) -> [Mocks](mocks/README.md) -> [Quizzes](quizzes/README.md) -> [Cheatsheets](cheatsheets/README.md) -> [Capstone Projects](capstone-projects/README.md)

## Progress Checklist

- [ ] Finish `fundamentals/` and complete one retrieval practice item.
- [ ] Finish `math/` and complete one retrieval practice item.
- [ ] Finish `statistics/` and complete one retrieval practice item.
- [ ] Finish `data-science/` and complete one retrieval practice item.
- [ ] Finish `classical-ml/` and complete one retrieval practice item.
- [ ] Finish `deep-learning/` and complete one retrieval practice item.
- [ ] Finish `nlp/` and complete one retrieval practice item.
- [ ] Finish `computer-vision/` and complete one retrieval practice item.
- [ ] Finish `recommender-systems/` and complete one retrieval practice item.
- [ ] Finish `mlops/` and complete one retrieval practice item.
- [ ] Finish `generative-ai/` and complete one retrieval practice item.
- [ ] Finish `llms/` and complete one retrieval practice item.
- [ ] Finish `vector-databases/` and complete one retrieval practice item.
- [ ] Finish `rag/` and complete one retrieval practice item.
- [ ] Finish `agents/` and complete one retrieval practice item.
- [ ] Finish `production-ai/` and complete one retrieval practice item.
- [ ] Finish `machine-learning-system-design/` and complete one retrieval practice item.
- [ ] Complete at least five case studies.
- [ ] Complete at least three mock interviews.
- [ ] Finish one capstone project with a written evaluation report.

## Using Quizzes

Use quizzes for retrieval practice, not passive reading. Answer first, then check the key and write a
one-sentence correction for every miss.

## Using Cheatsheets

Use cheatsheets before interviews and project work. They are compact references for concepts,
metrics, traps, and answer structure.

## Using Mocks

Use mocks to practice the full interview loop: clarification, baseline, design, evaluation,
tradeoffs, and self-review. Score yourself against the rubric and repeat weak rounds.

## Using Projects and Case Studies

Case studies show how to reason about real systems. Capstone projects turn that reasoning into
implementation practice. For each project, write down the problem, dataset, baseline, metric, error
analysis, production risks, and interview explanation.

## Repository Tools

- `python tools/generate_repo_index.py` refreshes [REPO_INDEX.md](REPO_INDEX.md).
- `python tools/check_links.py` validates local Markdown links.
- `python tools/check_markdown_quality.py` validates structure, naming, navigation, and formatting.
- `python tools/fix_markdown_formatting.py` applies safe formatting and navigation normalization.

## Repository Scope

This repository is maintained for personal study and interview preparation. It is not structured as a
community-maintained open-source project. The root is intentionally kept focused on learning paths,
reference material, practice, projects, and validation tools.

## Quality Promise

This repository aims to be practical, readable, and honest about tradeoffs. Content should teach from
first principles, connect to real engineering work, include practice, and avoid marketing language or
unsupported claims.
