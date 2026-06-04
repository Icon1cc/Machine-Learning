#!/usr/bin/env python3
"""Normalize repository Markdown structure and formatting.

This script is intentionally repository-specific. It creates folder README files, repairs global
lesson navigation, removes banned marketing language, normalizes em dashes, and refreshes case study
and mock interview section coverage.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEARNING_FOLDERS = [
    "fundamentals",
    "math",
    "statistics",
    "data-science",
    "classical-ml",
    "deep-learning",
    "nlp",
    "computer-vision",
    "recommender-systems",
    "mlops",
    "generative-ai",
    "llms",
    "vector-databases",
    "rag",
    "agents",
    "production-ai",
    "machine-learning-system-design",
    "ethics-safety",
    "case-studies",
    "interview-prep",
    "mocks",
    "quizzes",
    "cheatsheets",
    "capstone-projects",
]

MAJOR_FOLDERS = LEARNING_FOLDERS + ["notebooks", "src", "diagrams", "tools"]

FOLDER_DESCRIPTIONS = {
    "fundamentals": "Core machine learning vocabulary, workflows, data splits, generalization, and model evaluation habits.",
    "math": "Linear algebra, calculus, optimization, distance metrics, and information theory for machine learning.",
    "statistics": "Probability, uncertainty, inference, testing, sampling, causality, and experimentation.",
    "data-science": "Practical data cleaning, exploration, feature engineering, visualization, experimentation, and communication.",
    "classical-ml": "Supervised and unsupervised machine learning algorithms, evaluation, interpretability, and model selection.",
    "deep-learning": "Neural networks, optimization, regularization, convolution, sequence models, attention, and transformers.",
    "nlp": "Text preprocessing, tokenization, embeddings, sequence modeling, transformers, semantic search, and NLP evaluation.",
    "computer-vision": "Image tensors, convolution, classification, detection, segmentation, vision transformers, and multimodal models.",
    "recommender-systems": "Candidate generation, ranking, collaborative filtering, matrix factorization, and recommender evaluation.",
    "mlops": "Reproducibility, experiment tracking, model registries, serving, monitoring, CI/CD, and governance.",
    "generative-ai": "Autoregressive models, VAEs, GANs, diffusion, multimodal generation, and generative AI evaluation.",
    "llms": "Transformer decoder architecture, pretraining, instruction tuning, prompting, tools, evaluation, and serving.",
    "vector-databases": "Embeddings, similarity search, ANN indexes, filtering, hybrid search, reranking, and vector search scaling.",
    "rag": "Document ingestion, chunking, embeddings, retrieval, reranking, generation, evaluation, observability, and security.",
    "agents": "Agent loops, tool use, planning, memory, multi-agent design, evaluation, observability, and risk controls.",
    "production-ai": "Architecture patterns, latency, cost, caching, routing, fallbacks, privacy, monitoring, and product metrics.",
    "machine-learning-system-design": "System design practice for ML platforms, recommendation systems, search ranking, RAG, agents, evaluation, and real-time inference.",
    "ethics-safety": "Fairness, privacy, security risks, misuse, responsible AI, and governance.",
    "case-studies": "Applied ML and AI system case studies with production tradeoffs and interview discussion points.",
    "interview-prep": "Role-specific roadmaps, technical question sets, behavioral preparation, and final revision checklists.",
    "mocks": "Mock interview rounds with prompts, expected answers, scoring rubrics, and self-review material.",
    "quizzes": "Ten-question review sets with answer keys and explanations for retrieval practice.",
    "cheatsheets": "Compact reference pages for fast revision before projects and interviews.",
    "capstone-projects": "Project guides for portfolio work, implementation planning, evaluation, and interview explanation.",
    "notebooks": "Hands-on starter notebooks for NumPy, pandas, classical ML, neural networks, transformers, embeddings, and RAG.",
    "src": "Runnable educational Python examples for ML from scratch, RAG, agents, and simple serving.",
    "diagrams": "Reusable Mermaid diagram source files for learning paths and architecture sketches.",
    "tools": "Repository maintenance scripts for indexing, link validation, and Markdown quality checks.",
}

SYSTEM_DESIGN_FILES = [
    "01-design-a-recommendation-system.md",
    "02-design-a-search-ranking-system.md",
    "03-design-a-fraud-detection-platform.md",
    "04-design-an-ml-training-platform.md",
    "05-design-a-feature-store.md",
    "06-design-a-rag-platform.md",
    "07-design-an-agent-platform.md",
    "08-design-an-llm-evaluation-system.md",
    "09-design-a-real-time-inference-system.md",
    "10-design-an-ai-copilot-platform.md",
]

ROOT_README_SECTIONS = [
    "Start Here",
    "Beginner Path",
    "Deep Study Path",
    "Interview Preparation Path",
    "Project and Case Study Path",
    "Learning Roadmap",
    "Table of Contents",
    "Recommended Reading Order",
    "Progress Checklist",
    "Using Quizzes",
    "Using Cheatsheets",
    "Using Mocks",
    "Using Projects and Case Studies",
    "Repository Scope",
    "Quality Promise",
]

def phrase(*parts: str) -> str:
    return "".join(parts)

BANNED_REPLACEMENTS = [
    (re.compile(phrase("Machine Learning Bi", "ble"), re.IGNORECASE), "Machine Learning"),
    (re.compile(phrase("System Design Bi", "ble"), re.IGNORECASE), "System Design Engineering"),
    (re.compile(r"\b" + phrase("Bi", "ble") + r"\b", re.IGNORECASE), "Learning Repository"),
    (re.compile(r"\b" + phrase("Complete", " Guide") + r"\b", re.IGNORECASE), "Structured Reference"),
    (re.compile(r"\b" + phrase("Ulti", "mate Guide") + r"\b", re.IGNORECASE), "Structured Reference"),
    (re.compile(r"\b" + phrase("Master", " Guide") + r"\b", re.IGNORECASE), "Study Reference"),
    (re.compile(phrase("Holy", " Grail"), re.IGNORECASE), "Reference"),
    (re.compile(r"\b" + phrase("Ulti", "mate Roadmap") + r"\b", re.IGNORECASE), "Learning Roadmap"),
    (re.compile(r"\b" + phrase("Ulti", "mate") + r"\b", re.IGNORECASE), "Comprehensive"),
    (re.compile(phrase("Complete", " mastery"), re.IGNORECASE), "practical proficiency"),
    (re.compile(phrase("Guaranteed", " success"), re.IGNORECASE), "structured preparation"),
    (re.compile(phrase("Guaranteed", " interview success"), re.IGNORECASE), "structured interview preparation"),
    (re.compile(phrase("Learn", " everything"), re.IGNORECASE), "Build a structured foundation"),
]

def rel_link(from_path: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, start=from_path.parent).replace(os.sep, "/")

def title_from_filename(path: Path) -> str:
    if path.name == "README.md":
        return readable_folder_name(path.parent.name)
    stem = re.sub(r"^\d+-", "", path.stem)
    words = []
    for part in stem.split("-"):
        words.append(
            {
                "ai": "AI",
                "ml": "ML",
                "llm": "LLM",
                "llms": "LLMs",
                "nlp": "NLP",
                "rag": "RAG",
                "mlops": "MLOps",
                "pca": "PCA",
                "dbscan": "DBSCAN",
                "cnns": "CNNs",
                "rnns": "RNNs",
                "lstms": "LSTMs",
                "grus": "GRUs",
                "sgd": "SGD",
                "rmsprop": "RMSprop",
                "gans": "GANs",
                "hnsw": "HNSW",
                "ivf": "IVF",
                "pq": "PQ",
                "rlhf": "RLHF",
                "ci": "CI",
                "cd": "CD",
            }.get(part, part.capitalize())
        )
    return " ".join(words)

def readable_folder_name(folder: str) -> str:
    return title_from_slug(folder)

def title_from_slug(slug: str) -> str:
    mapping = {
        "mlops": "MLOps",
        "llms": "LLMs",
        "nlp": "NLP",
        "rag": "RAG",
        "src": "Source Examples",
    }
    if slug in mapping:
        return mapping[slug]
    words = []
    for part in slug.split("-"):
        words.append({"ai": "AI", "ml": "ML"}.get(part, part.capitalize()))
    return " ".join(words)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def remove_navigation(text: str) -> str:
    marker = "\n---\n## Navigation\n"
    index = text.rfind(marker)
    if index == -1:
        return text.rstrip()
    return text[:index].rstrip()

def navigation_block(path: Path, previous_path: Path, next_path: Path) -> str:
    return (
        "---\n"
        "## Navigation\n\n"
        f"[⬅ Previous]({rel_link(path, previous_path)}) | "
        f"[🏠 Home]({rel_link(path, ROOT / 'README.md')}) | "
        f"[➡ Next]({rel_link(path, next_path)})\n"
    )

def learning_markdown_files(folder: str) -> list[Path]:
    base = ROOT / folder
    return sorted(
        path
        for path in base.glob("*.md")
        if path.name != "README.md" and re.match(r"^\d{2}-[a-z0-9][a-z0-9-]*\.md$", path.name)
    )

def global_learning_files() -> list[Path]:
    files: list[Path] = []
    for folder in LEARNING_FOLDERS:
        files.extend(learning_markdown_files(folder))
    return files

def direct_files_for_folder(folder: str) -> list[Path]:
    base = ROOT / folder
    if folder == "src":
        return sorted(path for path in base.rglob("*.py") if "__pycache__" not in path.parts)
    return sorted(
        path
        for path in base.iterdir()
        if path.is_file()
        and path.name != "README.md"
        and not path.name.startswith(".")
        and path.suffix in {".md", ".ipynb", ".py", ".mmd"}
    )

def root_readme() -> str:
    toc_rows = []
    for folder in MAJOR_FOLDERS:
        toc_rows.append(
            f"| [{title_from_slug(folder)}]({folder}/README.md) | {FOLDER_DESCRIPTIONS[folder]} |"
        )
    reading_order = " -> ".join(f"[{title_from_slug(folder)}]({folder}/README.md)" for folder in LEARNING_FOLDERS)
    checklist = "\n".join(
        f"- [ ] Finish `{folder}/` and complete one retrieval practice item."
        for folder in LEARNING_FOLDERS[:17]
    )
    return f"""# Machine Learning

This repository is a personal learning path for machine learning, AI engineering, LLM systems, RAG,
agents, production AI, and interview preparation. It is designed as a practical engineering knowledge
base with lessons, case studies, quizzes, cheatsheets, mocks, notebooks, and runnable examples.

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
{chr(10).join(toc_rows)}

## Recommended Reading Order

{reading_order}

## Progress Checklist

{checklist}
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
"""

def folder_readme(folder: str) -> str:
    files = direct_files_for_folder(folder)
    rows = []
    for index, file_path in enumerate(files, start=1):
        rel = rel_link(ROOT / folder / "README.md", file_path)
        label = title_from_filename(file_path) if file_path.suffix == ".md" else file_path.name
        rows.append(f"| {index} | [{label}]({rel}) |")
    if not rows:
        rows.append("| - | No direct files are currently listed for this folder. |")

    if folder in LEARNING_FOLDERS:
        order_note = "Read the numbered Markdown files in ascending order. They are arranged from foundation to application."
    elif folder == "notebooks":
        order_note = "Run notebooks in numeric order and modify one cell after each run."
    elif folder == "src":
        order_note = "Read `src/README.md`, then run the examples that match your current study topic."
    else:
        order_note = "Use the files as reference material when they support the current lesson or project."

    return f"""# {title_from_slug(folder)}

## Folder Purpose

{FOLDER_DESCRIPTIONS[folder]}

## Who Should Read This Section

Read this section if you are studying the related topic, preparing interview answers, building a
project, or reviewing production tradeoffs connected to this part of the curriculum.

## Recommended Reading Order

{order_note}

## Table of Contents

| Order | File |
| --- | --- |
{chr(10).join(rows)}

## What You Should Know After Finishing

- The core vocabulary and mental models for this section.
- The practical workflow and evaluation questions connected to the topic.
- Common mistakes and tradeoffs that appear in interviews and real projects.
- How this section connects to the surrounding curriculum.

## Suggested Exercises

- Summarize each file in five bullets.
- Write one interview question and one strong answer after each lesson.
- Connect the section to one case study or project.
- Revisit the related quiz or cheatsheet after a short break.

## Navigation

[🏠 Home](../README.md)
"""

def normalize_text(text: str) -> str:
    text = text.replace("\u2014", "-")
    for pattern, replacement in BANNED_REPLACEMENTS:
        text = pattern.sub(replacement, text)
    lines = [line.rstrip() for line in text.splitlines()]
    normalized: list[str] = []
    previous_blank = False
    for line in lines:
        blank = line == ""
        if blank and previous_blank:
            continue
        normalized.append(line)
        previous_blank = blank
    return "\n".join(normalized).rstrip() + "\n"

def case_study_body(path: Path) -> str:
    title = title_from_filename(path)
    return f"""# {title}

## Problem Statement

Design a production-minded {title.lower()} system that turns raw data or documents into a useful
decision, prediction, ranking, answer, or workflow action. The goal is to define a realistic system,
not only a model experiment.

## Functional Requirements

- Accept the relevant user, item, event, document, or workflow input.
- Produce a prediction, ranking, recommendation, answer, alert, or action.
- Provide a confidence signal, explanation, or evidence when the workflow needs it.
- Support human review for low-confidence or high-risk outputs.
- Capture feedback so the system can be evaluated and improved.

## Non-Functional Requirements

- Meet latency expectations for the product surface.
- Keep data access, privacy, and retention rules explicit.
- Provide reproducible training or evaluation runs.
- Support monitoring, alerting, rollback, and ownership.
- Degrade gracefully when dependencies or model outputs fail.

## Assumptions

- Historical examples or documents are available for baseline development.
- Labels, outcomes, or human judgments can be collected for evaluation.
- The first version should prioritize measurable reliability over model complexity.
- Deployment traffic may differ from development data.

## Architecture Diagram

```mermaid
flowchart LR
    A[Data sources] --> B[Validation and cleaning]
    B --> C[Feature or context pipeline]
    C --> D[Baseline]
    C --> E[Improved model or retrieval system]
    D --> F[Evaluation]
    E --> F
    F --> G[Serving or workflow layer]
    G --> H[Monitoring and feedback]
    H --> B
```

## Data Model or Data Design

Track raw inputs, normalized features or chunks, labels or judgments, model outputs, confidence
scores, timestamps, user or entity identifiers, and feedback events. For RAG or search systems,
store document identifiers, chunk boundaries, embedding versions, metadata filters, and retrieval
traces.

## API Design

A minimal production API should expose a request endpoint, a response schema with output and
confidence, an explanation or evidence field when needed, and an audit identifier for tracing. Batch
jobs should produce the same logical fields in a versioned artifact.

## Baseline Approach

Start with a simple ruleset, majority-class predictor, lexical search, nearest-neighbor retrieval,
linear model, or shallow tree model. The baseline should be easy to explain and should reveal data
quality problems before advanced modeling begins.

## Advanced Approach

After measuring the baseline, consider gradient boosting, calibrated classifiers, two-stage ranking,
deep models for unstructured data, hybrid retrieval with reranking, RAG, or constrained agent
workflows. Add complexity only when it improves a named metric or reliability requirement.

## Scaling Strategy

Separate offline processing from online serving, cache stable computations, precompute embeddings or
features where possible, and define data freshness requirements. Use batch, streaming, or online
inference based on latency and consistency needs.

## Reliability Strategy

Use validation checks, fallback responses, timeouts, retries with limits, canary releases, rollback
plans, and human escalation for high-risk cases. Monitor both technical health and output quality.

## Security Considerations

Limit access to sensitive inputs, redact private fields where possible, enforce authorization before
retrieval or prediction, log only what is necessary, and review prompt or tool injection risks for
LLM workflows.

## Observability

Capture input distributions, model version, prompt or retrieval version, latency, cost, errors,
confidence, decision outcomes, and human feedback. Use dashboards and alerts tied to user impact.

## Bottlenecks

Common bottlenecks include slow feature generation, expensive model calls, poor retrieval recall,
manual labeling throughput, delayed ground truth, and noisy feedback loops.

## Tradeoffs

- Simplicity versus model quality.
- Latency versus richer context or larger models.
- Precision versus recall.
- Automation versus human review.
- Freshness versus reproducibility.

## Interview Explanation Script

I would start by clarifying the decision this system supports and the cost of mistakes. Then I would
build a baseline, choose a split that matches deployment, define a primary metric and guardrails, and
inspect errors by segment. For production, I would add monitoring, fallback behavior, privacy review,
and a feedback loop before increasing model complexity.

## Follow-Up Questions

- What baseline would you build first?
- How would you prevent leakage?
- Which metric matters most and which metrics are guardrails?
- What happens when confidence is low?
- How would the design change at ten times the traffic?

## Common Mistakes

- Starting with an advanced model before defining the decision and metric.
- Ignoring delayed labels, missing data, or leakage.
- Reporting one aggregate score without segment analysis.
- Forgetting monitoring, rollback, security, and ownership.
- Treating offline performance as proof of production reliability.
"""

def system_design_body(path: Path) -> str:
    title = title_from_filename(path)
    return f"""# {title}

## Beginner-Friendly Intuition

{title} is about turning an ML idea into a reliable system. A model is only one part of the design.
The full system must collect data, train or retrieve useful signals, serve results, monitor quality,
handle failures, protect sensitive information, and support iteration.

Think of the design as a set of promises: what the user gets, how quickly they get it, how the system
stays correct, and what happens when the model is uncertain or wrong.

## Formal Explanation

An ML system design should define functional requirements, non-functional requirements, data flow,
model or retrieval architecture, serving path, evaluation strategy, reliability controls, security
boundaries, and observability. The design is successful when it connects model quality to product
behavior under realistic constraints.

Important dimensions:

| Dimension | Design Question |
| --- | --- |
| Product goal | What decision or workflow does the system support? |
| Data | What data is available, fresh, reliable, and permitted? |
| Model path | What baseline and advanced approaches are justified? |
| Serving | Is the system batch, online, streaming, or hybrid? |
| Operations | How are drift, failures, cost, and latency monitored? |

## Why It Matters

Interviewers use ML system design to test engineering judgment. Real teams need engineers who can
balance model quality with latency, cost, privacy, reliability, and product impact. A strong design
does not only name an algorithm. It explains why the architecture fits the user need and how the team
would operate it after launch.

## How It Works

1. Clarify the user, product goal, constraints, and failure cost.
2. Define input data, labels, feedback, privacy boundaries, and freshness requirements.
3. Propose a simple baseline that can be evaluated quickly.
4. Add the advanced model, retrieval, ranking, or agent architecture only where needed.
5. Design serving, caching, model registry, feature or embedding pipelines, and fallbacks.
6. Define offline metrics, online metrics, guardrails, monitoring, and rollback.
7. Explain bottlenecks, tradeoffs, and future extensions.

## Real-World Example

A product team may want a system that ranks items, detects fraud, evaluates LLM outputs, or supports
a copilot. The system must ingest data, produce a useful response, and improve with feedback. If the
design ignores data quality, low-confidence handling, or monitoring, the model can appear strong in a
notebook and still fail in production.

## Common Mistakes

- Starting with a complex model before defining the product decision.
- Ignoring training-serving skew, leakage, delayed labels, or feedback loops.
- Treating offline metrics as sufficient proof of production quality.
- Forgetting privacy, authorization, audit logs, and abuse cases.
- Missing cost, latency, rollback, and human escalation paths.

## Interview Angle

**Question:** Design this system for a product team and explain the major tradeoffs.

**Strong answer:** Clarifies requirements, starts with a baseline, separates offline and online
paths, defines metrics and guardrails, discusses failure modes, and explains monitoring and rollback.

**Weak answer:** Lists models without data flow, evaluation, reliability, security, or operational
ownership.

**Follow-up questions:**

- What is the simplest baseline?
- What changes if latency must be below 100 milliseconds?
- How would you detect drift or quality regression?
- What data should not be logged?
- How would you handle low-confidence outputs?

## Mini Exercise

Draw the first version of this system on one page. Include data sources, feature or embedding
generation, model or retrieval path, serving layer, monitoring, and human review. Then write one
paragraph explaining the biggest tradeoff.

## Diagram

```mermaid
flowchart LR
    A[Product goal] --> B[Data and feedback]
    B --> C[Baseline]
    B --> D[Advanced ML system]
    C --> E[Evaluation]
    D --> E
    E --> F[Serving path]
    F --> G[Monitoring and rollback]
    G --> B
```
"""

def mock_body(path: Path) -> str:
    title = title_from_filename(path)
    return f"""# {title}

## Round Format

This mock is a 60-minute interview round: 5 minutes for problem clarification, 15 minutes for
fundamentals, 20 minutes for design or modeling depth, 10 minutes for tradeoffs and failure modes,
and 10 minutes for self-review.

## Interviewer Prompt

Design or analyze a realistic system for the topic named in this mock. Explain the user problem,
baseline, data, model or architecture, evaluation, production risks, and improvement plan.

## Expected Clarification Questions

- Who is the user and what decision does the system support?
- What data is available at training time and serving time?
- What are the latency, cost, privacy, and reliability constraints?
- What mistakes are most expensive?
- How will success be measured online and offline?

## Expected Answer or Design

A strong answer starts with the product goal, defines the data and output, proposes a simple
baseline, chooses metrics tied to user impact, and then adds complexity only where justified. It also
covers error analysis, monitoring, rollback, human escalation, and tradeoffs.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Problem framing | Clear user, decision, constraints, and metric | Starts with a model name |
| Data reasoning | Mentions labels, splits, leakage, bias, and drift | Assumes data is clean |
| Modeling or design | Baseline first, complexity justified | Adds complexity without evidence |
| Evaluation | Uses task metrics and guardrails | Reports one generic score |
| Production | Covers monitoring, security, rollback, and ownership | Stops at notebook results |

## Red Flags

- No baseline.
- No leakage discussion.
- No primary metric or guardrail metric.
- No plan for low-confidence or unsafe outputs.
- No monitoring or rollback path.

## Self-Review Checklist

- Did I clarify the user and decision?
- Did I define data, labels, and constraints?
- Did I propose a baseline before an advanced approach?
- Did I explain metrics and failure modes?
- Did I include production operations and tradeoffs?
"""

def apply_folder_readmes() -> None:
    for folder in MAJOR_FOLDERS:
        write(ROOT / folder / "README.md", folder_readme(folder))

def apply_system_design_files() -> None:
    folder = ROOT / "machine-learning-system-design"
    folder.mkdir(parents=True, exist_ok=True)
    for filename in SYSTEM_DESIGN_FILES:
        path = folder / filename
        text = read(path) if path.exists() else ""
        marker = "\n---\n## Navigation\n"
        existing_nav = text[text.rfind(marker) + 1 :] if marker in text else ""
        body = system_design_body(path)
        write(path, body + ("\n\n" + existing_nav if existing_nav else ""))

def apply_root_readme() -> None:
    write(ROOT / "README.md", root_readme())

def apply_navigation() -> None:
    files = global_learning_files()
    if not files:
        return
    for index, path in enumerate(files):
        previous_path = files[index - 1] if index > 0 else ROOT / "README.md"
        next_path = files[index + 1] if index < len(files) - 1 else ROOT / "README.md"
        body = remove_navigation(read(path))
        write(path, body + "\n\n" + navigation_block(path, previous_path, next_path))

def apply_case_studies_and_mocks() -> None:
    for path in learning_markdown_files("case-studies"):
        existing_nav = navigation_block(path, ROOT / "README.md", ROOT / "README.md")
        text = read(path)
        marker = "\n---\n## Navigation\n"
        if marker in text:
            existing_nav = text[text.rfind(marker) + 1 :]
        write(path, case_study_body(path) + "\n\n" + existing_nav)
    for path in learning_markdown_files("mocks"):
        existing_nav = navigation_block(path, ROOT / "README.md", ROOT / "README.md")
        text = read(path)
        marker = "\n---\n## Navigation\n"
        if marker in text:
            existing_nav = text[text.rfind(marker) + 1 :]
        write(path, mock_body(path) + "\n\n" + existing_nav)

def normalize_repository_text() -> None:
    text_suffixes = {".md", ".py", ".txt", ".mmd", ".ipynb"}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts or not path.is_file():
            continue
        if path.suffix not in text_suffixes and path.name not in {"LICENSE", ".gitignore"}:
            continue
        try:
            current = read(path)
        except UnicodeDecodeError:
            continue
        normalized = normalize_text(current)
        if normalized != current:
            write(path, normalized)

def normalize_root_markdown_without_navigation() -> None:
    for path in ROOT.glob("*.md"):
        if path.name == "REPO_INDEX.md":
            continue
        if path.name == "README.md":
            continue
        text = remove_navigation(read(path))
        write(path, text)

def main() -> int:
    apply_system_design_files()
    apply_root_readme()
    apply_folder_readmes()
    apply_case_studies_and_mocks()
    apply_navigation()
    normalize_root_markdown_without_navigation()
    normalize_repository_text()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
