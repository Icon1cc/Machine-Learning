# Machine Learning Bible

Start here: [What Is Machine Learning?](fundamentals/01-what-is-machine-learning.md)

## Purpose

Machine Learning Bible is a complete, GitHub-ready self-study repository for moving from absolute
basics to interview-ready AI, ML, LLM, and production AI engineering. It is designed to be useful
offline: concepts, examples, quizzes, case studies, project guides, notebooks, and runnable source
code are stored directly in this repository.

## Who This Is For

- Future AI Engineers, Machine Learning Engineers, LLM Engineers, Data Scientists, Applied
  Scientists, and GenAI Engineers.
- Software engineers who want to move into ML or AI product engineering.
- Students who understand programming but need a practical map from first principles to interviews.
- Practitioners who want structured revision material before technical screens and system design
  interviews.

## How to Use It

Read in numeric order inside each folder. Build projects as you learn rather than saving practice for
the end. After each major phase, do one quiz, one case study, and one project writeup. Use the source
examples to make abstract ideas concrete.

## Mermaid Learning Roadmap

```mermaid
flowchart LR
    Basics --> Math --> Statistics --> Python_and_Data[Python and Data] --> Classical_ML[Classical ML]
    Classical_ML --> Deep_Learning[Deep Learning] --> NLP --> Computer_Vision[Computer Vision]
    Computer_Vision --> Recommenders --> MLOps --> GenAI --> LLMs
    LLMs --> Vector_Databases[Vector Databases] --> RAG --> Agents
    Agents --> Production_AI[Production AI] --> Interviews --> Capstones
```

## 12-Week Fast Track

| Weeks | Focus | Outcome |
| --- | --- | --- |
| 1-2 | Fundamentals, math, statistics | Explain core ML vocabulary and uncertainty |
| 3-4 | Data science and classical ML | Build tabular baselines and evaluate them |
| 5-6 | Deep learning, NLP, computer vision | Understand neural architectures and training |
| 7-8 | Recommenders, MLOps, production AI | Design reliable ML systems |
| 9-10 | GenAI, LLMs, vector databases, RAG | Build grounded LLM applications |
| 11 | Agents and safety | Design constrained tool-using systems |
| 12 | Interviews and capstones | Practice full-loop interview explanations |

## 24-Week Deep Track

Spend one week on each major folder through `production-ai/`, then use the remaining weeks for case
studies, mocks, quizzes, and capstones. The deep track is slower because it includes repeated
implementation, error analysis, and interview narration.

## 6-Week Interview Revision Track

| Week | Focus |
| --- | --- |
| 1 | Fundamentals, statistics, and evaluation |
| 2 | Classical ML and feature engineering |
| 3 | Deep learning, transformers, NLP, and vision |
| 4 | LLMs, RAG, vector databases, and agents |
| 5 | MLOps, production AI, case studies, and system design |
| 6 | Mock interviews, cheatsheets, and final revision checklist |

## Project-First Track

Choose a capstone first, then read only the files needed to unblock the next implementation step.
This is the best route if you learn by building. Use [PROJECTS.md](PROJECTS.md) and
[capstone-projects/](capstone-projects/) as your home base.

## Table of Contents

- [fundamentals/](fundamentals/)
- [math/](math/)
- [statistics/](statistics/)
- [data-science/](data-science/)
- [classical-ml/](classical-ml/)
- [deep-learning/](deep-learning/)
- [nlp/](nlp/)
- [computer-vision/](computer-vision/)
- [recommender-systems/](recommender-systems/)
- [mlops/](mlops/)
- [generative-ai/](generative-ai/)
- [llms/](llms/)
- [vector-databases/](vector-databases/)
- [rag/](rag/)
- [agents/](agents/)
- [production-ai/](production-ai/)
- [ethics-safety/](ethics-safety/)
- [case-studies/](case-studies/)
- [interview-prep/](interview-prep/)
- [mocks/](mocks/)
- [quizzes/](quizzes/)
- [cheatsheets/](cheatsheets/)
- [capstone-projects/](capstone-projects/)
- [notebooks/](notebooks/)
- [src/](src/)
- [diagrams/](diagrams/)
- [tools/](tools/)

## Recommended Reading Order

fundamentals -> math -> statistics -> data-science -> classical-ml -> deep-learning -> nlp -> computer-vision -> recommender-systems -> mlops -> generative-ai -> llms -> vector-databases -> rag -> agents -> production-ai -> interview-prep -> capstone-projects

## Main Practice Loop

1. Read one lesson.
2. Explain it out loud in beginner language.
3. Complete the mini exercise.
4. Run or modify one notebook or source example.
5. Answer related quiz questions.
6. Add the idea to a project or case study explanation.

## Repository Tools

- `python tools/generate_repo_index.py` creates [REPO_INDEX.md](REPO_INDEX.md).
- `python tools/check_links.py` validates local Markdown links.

## Definition of Done for Self-Study

You are interview-ready on a topic when you can define it, derive or trace the core mechanism, build a
baseline, choose metrics, identify failure modes, explain production concerns, and discuss tradeoffs
without reading notes.

---
## Navigation

[⬅ Previous](README.md) | [🏠 Home](README.md) | [➡ Next](ROADMAP.md)
