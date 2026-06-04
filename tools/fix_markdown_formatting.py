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

CASE_STUDY_DETAILS = {
    "spam-classifier": {
        "domain": "email and message moderation",
        "inputs": "message body, subject, sender reputation, links, attachments, and user reports",
        "output": "spam, likely spam, or clean with a calibrated confidence score",
        "baseline": "keyword rules, deny lists, sender reputation checks, and a logistic regression model over TF-IDF features",
        "advanced": "gradient boosting over engineered sender signals plus a transformer text classifier for hard examples",
        "metric": "precision at high recall, false-positive rate on trusted senders, review volume, and complaint rate",
        "failure": "blocking a legitimate account recovery or business email",
    },
    "fraud-detection": {
        "domain": "payments and account risk",
        "inputs": "transaction amount, merchant, device, account age, velocity features, location, and prior disputes",
        "output": "approve, challenge, block, or route to review",
        "baseline": "velocity rules, allow and deny lists, and a calibrated tree model on tabular features",
        "advanced": "sequence features, graph signals across shared devices, and cost-sensitive gradient boosting",
        "metric": "fraud loss prevented, false decline rate, review precision, chargeback rate, and latency",
        "failure": "blocking a legitimate high-value payment during checkout",
    },
    "credit-risk-model": {
        "domain": "loan underwriting",
        "inputs": "application fields, credit history, income signals, debt ratios, and repayment outcomes",
        "output": "risk tier, approval recommendation, limit, or pricing band",
        "baseline": "scorecard rules and logistic regression with monotonic, explainable features",
        "advanced": "calibrated gradient boosting with fairness, stability, and adverse-action explanation checks",
        "metric": "default rate by risk band, approval rate, calibration, fairness gaps, and portfolio loss",
        "failure": "creating an unfair or unstable decision rule across protected or thin-file segments",
    },
    "customer-churn-prediction": {
        "domain": "subscription retention",
        "inputs": "usage history, billing events, support tickets, plan changes, tenure, and engagement trends",
        "output": "churn probability, risk segment, and suggested retention action",
        "baseline": "recency and usage rules plus logistic regression on account-level features",
        "advanced": "survival analysis or gradient boosting with time-windowed behavioral features",
        "metric": "lift in contacted segments, calibration, retention impact, intervention cost, and customer experience guardrails",
        "failure": "targeting users who would have stayed without intervention and wasting retention budget",
    },
    "recommendation-system": {
        "domain": "personalized content or product discovery",
        "inputs": "user events, item metadata, inventory state, impressions, clicks, purchases, and negative feedback",
        "output": "ranked candidates with reasons and diversity controls",
        "baseline": "popular items, recent items, collaborative filtering, and simple content similarity",
        "advanced": "two-stage retrieval and ranking with embeddings, learning-to-rank features, and exploration",
        "metric": "CTR, conversion, retention, diversity, freshness, coverage, and long-term satisfaction",
        "failure": "over-personalizing into a narrow loop that hurts discovery and trust",
    },
    "search-ranking-system": {
        "domain": "search relevance",
        "inputs": "query text, document fields, click logs, freshness, permissions, and result feedback",
        "output": "ranked search results with snippets and relevance scores",
        "baseline": "BM25 with field boosts, filters, and query normalization",
        "advanced": "hybrid lexical and vector retrieval followed by a learned reranker",
        "metric": "NDCG, MRR, zero-result rate, latency, abandonment, and judged relevance",
        "failure": "ranking inaccessible, stale, or wrong documents above the answer users need",
    },
    "ad-click-through-rate-prediction": {
        "domain": "ads ranking",
        "inputs": "ad features, user context, page context, bid, historical impressions, clicks, and conversions",
        "output": "click probability used by ranking or auction logic",
        "baseline": "regularized logistic regression over crossed categorical and numeric features",
        "advanced": "wide-and-deep or gradient boosted models with calibration and delayed-feedback correction",
        "metric": "log loss, calibration, revenue, user quality guardrails, and advertiser outcome metrics",
        "failure": "optimizing clicks that reduce user trust or advertiser value",
    },
    "time-series-forecasting": {
        "domain": "demand, traffic, or resource planning",
        "inputs": "timestamped observations, calendar features, promotions, outages, and external drivers",
        "output": "forecast with prediction intervals and anomaly flags",
        "baseline": "seasonal naive forecasts, moving averages, and simple regression on calendar features",
        "advanced": "gradient boosting, probabilistic forecasting, or sequence models with covariates",
        "metric": "MAE, WAPE, interval coverage, bias by segment, and business planning error",
        "failure": "missing a demand spike that causes stockouts or capacity incidents",
    },
    "document-classification": {
        "domain": "document routing and compliance triage",
        "inputs": "document text, layout metadata, source, language, and human labels",
        "output": "document class, confidence, and fields required for downstream routing",
        "baseline": "rules and TF-IDF linear models with human review for low confidence",
        "advanced": "layout-aware or transformer classifiers with active learning for uncertain classes",
        "metric": "macro F1, per-class recall, review load, routing latency, and audit error rate",
        "failure": "misrouting a regulated document that requires special handling",
    },
    "semantic-search-engine": {
        "domain": "meaning-based knowledge retrieval",
        "inputs": "queries, documents, metadata, embeddings, permissions, and click or judgment feedback",
        "output": "ranked passages or documents with matched evidence",
        "baseline": "BM25 plus metadata filters and manually tuned synonyms",
        "advanced": "dense retrieval, hybrid search, reranking, and query rewriting",
        "metric": "recall at k, MRR, judged relevance, latency, and permission violation rate",
        "failure": "retrieving semantically similar but factually wrong evidence",
    },
    "chatbot-with-rag": {
        "domain": "grounded question answering",
        "inputs": "user question, conversation state, retrieved passages, source metadata, and safety context",
        "output": "answer with citations, uncertainty, and escalation when evidence is missing",
        "baseline": "keyword retrieval plus extractive answer snippets",
        "advanced": "hybrid retrieval, reranking, context compression, and answer grounding checks",
        "metric": "answer faithfulness, citation precision, user resolution rate, latency, and refusal quality",
        "failure": "presenting an unsupported answer as if it came from the source material",
    },
    "enterprise-knowledge-assistant": {
        "domain": "internal company knowledge access",
        "inputs": "documents, permissions, freshness metadata, employee query, and audit context",
        "output": "permission-aware answer with source links and escalation options",
        "baseline": "permission-filtered search with snippets and manual source review",
        "advanced": "RAG with access-control filtering, reranking, answer validation, and feedback capture",
        "metric": "resolution rate, citation accuracy, permission correctness, freshness, and support deflection",
        "failure": "leaking restricted information across teams or roles",
    },
    "customer-support-agent": {
        "domain": "support automation",
        "inputs": "ticket text, account state, policy documents, prior cases, tools, and escalation rules",
        "output": "draft response, next action, or routed ticket with confidence and evidence",
        "baseline": "intent classifier, macro templates, and retrieval over support articles",
        "advanced": "tool-using agent with constrained actions, policy checks, and human approval gates",
        "metric": "first-contact resolution, escalation accuracy, handle time, CSAT, and safety incidents",
        "failure": "taking an account action without enough evidence or authorization",
    },
    "code-assistant": {
        "domain": "developer productivity",
        "inputs": "code context, repository metadata, tests, user request, and tool outputs",
        "output": "patch, explanation, test command, or code review finding",
        "baseline": "retrieval over files plus static suggestions without write access",
        "advanced": "agentic edit loop with test execution, diff review, and rollback-safe patching",
        "metric": "accepted changes, build pass rate, defect rate, latency, and developer review effort",
        "failure": "modifying unrelated code or introducing a hidden security regression",
    },
    "ai-meeting-summarizer": {
        "domain": "meeting notes and action tracking",
        "inputs": "transcript, speaker turns, calendar metadata, chat messages, and organization policy",
        "output": "summary, decisions, action items, owners, deadlines, and uncertainty markers",
        "baseline": "extractive notes using transcript sections and keyword action detection",
        "advanced": "LLM summarization with entity resolution, action extraction, and human correction feedback",
        "metric": "action-item precision, decision recall, edit distance from human notes, privacy compliance, and latency",
        "failure": "assigning an action to the wrong person or exposing confidential content",
    },
    "llm-evaluation-platform": {
        "domain": "LLM quality measurement",
        "inputs": "test prompts, expected criteria, model outputs, judge rubrics, traces, and human ratings",
        "output": "scorecards, regressions, failure clusters, and release recommendations",
        "baseline": "golden test sets with deterministic string and rubric checks",
        "advanced": "LLM-as-judge with calibration, pairwise comparison, and trace-level diagnostics",
        "metric": "judge agreement, regression detection, coverage, false alarm rate, and evaluation cost",
        "failure": "shipping a model change because the evaluation set missed a critical workflow",
    },
    "vector-search-at-scale": {
        "domain": "large-scale approximate nearest neighbor retrieval",
        "inputs": "embeddings, metadata, index versions, query vectors, filters, and relevance judgments",
        "output": "nearest candidates with scores, filters, and index trace metadata",
        "baseline": "exact search on a sample plus a simple HNSW index",
        "advanced": "sharded HNSW or IVF-PQ with hybrid filtering, reranking, and versioned rollouts",
        "metric": "recall at k, p95 latency, index build time, memory use, and freshness",
        "failure": "reducing recall during an index migration without detection",
    },
    "ml-monitoring-platform": {
        "domain": "model observability",
        "inputs": "prediction logs, features, labels, metrics, model versions, alerts, and incidents",
        "output": "dashboards, alerts, drift reports, and rollback recommendations",
        "baseline": "batch metrics over prediction logs and simple threshold alerts",
        "advanced": "segment-aware drift detection, delayed-label quality tracking, and incident workflows",
        "metric": "time to detect, false alert rate, coverage by model, incident duration, and owner response",
        "failure": "missing a silent quality regression because labels arrive late",
    },
    "personalization-engine": {
        "domain": "personalized product experience",
        "inputs": "user profile, behavior history, context, catalog metadata, constraints, and feedback",
        "output": "personalized layout, ranking, message, or offer with guardrails",
        "baseline": "rules, segments, popularity, and recency-based recommendations",
        "advanced": "contextual ranking with exploration, diversity constraints, and causal measurement",
        "metric": "engagement lift, conversion, retention, diversity, opt-out rate, and long-term value",
        "failure": "optimizing short-term clicks while hurting long-term user satisfaction",
    },
    "ai-agent-for-workflows": {
        "domain": "workflow automation",
        "inputs": "user goal, available tools, permissions, task state, documents, and approval policy",
        "output": "completed task, plan, tool trace, or escalation request",
        "baseline": "deterministic workflow with forms, rules, and manual approvals",
        "advanced": "tool-using agent with planning limits, state tracking, validation, and human checkpoints",
        "metric": "task success rate, intervention rate, unsafe action rate, latency, and auditability",
        "failure": "calling a tool that changes state without the required approval",
    },
}

CAPSTONE_DETAILS = {
    "end-to-end-classical-ml-project": ("tabular prediction", "structured rows with labels", "simple linear or tree baseline", "gradient boosting with error analysis", "F1, calibration, and segment performance"),
    "house-price-prediction": ("real estate pricing", "property attributes, location, and sale price", "median-by-neighborhood baseline", "regularized regression or gradient boosting", "MAE and error by price band"),
    "fraud-detection-system": ("transaction risk", "payments, account metadata, device signals, and labels", "rules plus logistic regression", "cost-sensitive gradient boosting", "fraud loss, false declines, and review precision"),
    "customer-churn-prediction": ("subscription retention", "usage, billing, support, and churn labels", "recency and usage rules", "survival or gradient boosted model", "lift, calibration, and intervention cost"),
    "recommendation-system": ("personalized discovery", "user events, item metadata, and feedback", "popular and recent items", "candidate retrieval plus ranking", "CTR, conversion, diversity, and retention"),
    "search-ranking-system": ("search relevance", "queries, documents, clicks, and judgments", "BM25 with filters", "hybrid retrieval plus reranking", "NDCG, MRR, zero-result rate, and latency"),
    "image-classifier": ("image classification", "labeled images and augmentation metadata", "simple CNN or transfer-learning baseline", "fine-tuned vision backbone", "accuracy, macro F1, and class-level recall"),
    "nlp-text-classifier": ("text classification", "documents, labels, metadata, and language signals", "TF-IDF linear model", "fine-tuned transformer", "macro F1, calibration, and per-class recall"),
    "semantic-search-engine": ("semantic retrieval", "documents, queries, embeddings, and relevance judgments", "BM25 search", "dense retrieval with reranking", "recall at k, MRR, and p95 latency"),
    "rag-chatbot": ("grounded answering", "documents, chunks, queries, and feedback", "keyword retrieval with snippets", "RAG with hybrid retrieval and citations", "faithfulness, citation precision, and latency"),
    "enterprise-rag-assistant": ("permission-aware knowledge access", "documents, ACLs, queries, and audit logs", "permission-filtered search", "RAG with reranking and source validation", "answer quality, access correctness, and freshness"),
    "llm-evaluation-dashboard": ("LLM release evaluation", "prompts, outputs, rubrics, traces, and human scores", "golden test set checks", "judge-assisted scorecards with calibration", "judge agreement, regression detection, and cost"),
    "agentic-research-assistant": ("research workflow support", "user goals, sources, notes, and tool traces", "retrieval plus structured notes", "bounded agent with citations and review steps", "task success, citation accuracy, and unsafe action rate"),
    "ai-customer-support-agent": ("support automation", "tickets, policies, account context, tools, and outcomes", "intent routing and templates", "tool-using agent with approval gates", "resolution rate, escalation accuracy, and safety incidents"),
    "production-ml-platform": ("shared ML infrastructure", "training jobs, features, models, metrics, and deployments", "scripts and manual deployment checklist", "tracked pipelines, registry, serving, and monitoring", "reproducibility, deployment frequency, and incident rate"),
}

INTERVIEW_PREP_DETAILS = {
    "ai-engineer-roadmap": "AI product engineering, LLM application design, evaluation, safety, and production tradeoffs",
    "ml-engineer-roadmap": "modeling, data pipelines, training-serving consistency, deployment, and monitoring",
    "llm-engineer-roadmap": "prompting, RAG, fine-tuning choices, evaluation, serving cost, and guardrails",
    "data-scientist-roadmap": "experimentation, statistics, business metrics, modeling, and communication",
    "common-ml-interview-questions": "core ML reasoning across data, baselines, evaluation, and production failure modes",
    "statistics-interview-questions": "probability, inference, A/B testing, uncertainty, leakage, and causal reasoning",
    "classical-ml-interview-questions": "linear models, trees, ensembles, clustering, evaluation, and interpretability",
    "deep-learning-interview-questions": "optimization, backpropagation, regularization, architectures, and debugging",
    "llm-interview-questions": "tokenization, transformers, prompting, tool use, evaluation, and serving",
    "rag-interview-questions": "ingestion, chunking, retrieval, reranking, grounding, evaluation, and security",
    "agent-interview-questions": "agent loops, tools, planning, memory, observability, and approval boundaries",
    "ml-system-design-interview-questions": "requirements, data flow, model architecture, serving, monitoring, and rollback",
    "behavioral-ai-interviews": "project storytelling, ownership, ambiguity, tradeoff communication, and failure reflection",
    "resume-project-strategy": "project selection, scope, metrics, impact framing, and interview-ready explanation",
    "final-revision-checklist": "last-pass review across fundamentals, systems, projects, mocks, and weak spots",
}

ROOT_README_SECTIONS = [
    "Purpose",
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
    return " ".join(words).replace("End To End", "End-to-End")

def content_slug(path: Path) -> str:
    return re.sub(r"^\d+-", "", path.stem)

def sentence_label(title: str) -> str:
    label = title.lower()
    replacements = {
        "end to end": "end-to-end",
        " ai ": " AI ",
        "ai ": "AI ",
        " llm": " LLM",
        " ml ": " ML ",
        "ml ": "ML ",
        " nlp ": " NLP ",
        "nlp ": "NLP ",
        " rag": " RAG",
        "rag ": "RAG ",
    }
    for source, replacement in replacements.items():
        label = label.replace(source, replacement)
    return label

def indefinite_article(label: str) -> str:
    lower_label = label.lower()
    if lower_label.startswith(("ai", "end-to-end", "image", "llm", "ml", "nlp")):
        return "an"
    return "a"

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
    details = CASE_STUDY_DETAILS.get(content_slug(path), {})
    domain = details.get("domain", title.lower())
    inputs = details.get("inputs", "the most relevant user, item, event, document, and feedback signals")
    output = details.get("output", "a decision, score, ranking, answer, or workflow action")
    baseline = details.get("baseline", "a simple ruleset and a measurable model baseline")
    advanced = details.get("advanced", "a more capable model or retrieval design with explicit guardrails")
    metric = details.get("metric", "task quality, latency, cost, reliability, and user impact")
    failure = details.get("failure", "making an incorrect decision in a high-impact segment")
    return f"""# {title}

## Problem Statement

Design a production-minded {title.lower()} case study for {domain}. The system should use {inputs}
to produce {output}. The goal is to show how a practical ML or AI design moves from product framing
to data, modeling, evaluation, serving, monitoring, and human review.

## Domain Context

In this domain, the model is part of an operational decision. A strong design makes the cost of a
wrong output explicit, defines what data is available at decision time, and explains how the system
will recover when confidence is low. The highest-risk failure to plan around is {failure}.

## Functional Requirements

- Ingest {inputs}.
- Produce {output}.
- Provide confidence, evidence, or explanation when the workflow needs it.
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
scores, timestamps, entity identifiers, and feedback events. Include version fields for features,
models, prompts, retrieval indexes, and evaluation datasets so offline results can be compared with
production behavior.

## API Design

A minimal production API should accept the domain input, return the output, confidence, model
version, explanation or evidence when needed, and an audit identifier for tracing. Batch jobs should
produce the same logical fields in a versioned artifact so results can be replayed and inspected.

## Baseline Approach

Start with {baseline}. The baseline should be easy to explain, cheap to run, and strong enough to
expose data quality problems before advanced modeling begins.

## Advanced Approach

After measuring the baseline, consider {advanced}. Add complexity only when it improves a named
metric or reduces a known operational risk.

## Evaluation Plan

Evaluate with {metric}. Include slice analysis for important user, item, time, source, language, or
risk segments. Keep a small set of hard examples for regression checks and review disagreements
between model outputs and human judgment.

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
- Precision versus recall or relevance depth.
- Automation versus human review.
- Freshness versus reproducibility.

## Interview Explanation Script

I would start by clarifying the decision this system supports, the available data, and the cost of
{failure}. Then I would build {baseline}, define metrics around {metric}, inspect errors by segment,
and only then consider {advanced}. For production, I would add monitoring, fallback behavior, privacy
review, and a feedback loop before increasing automation.

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

def interview_prep_body(path: Path) -> str:
    title = title_from_filename(path)
    focus = INTERVIEW_PREP_DETAILS.get(content_slug(path), title.lower())
    return f"""# {title}

## How to Use This File

Use this page to practice structured interview answers for {focus}. Read each question, answer out
loud, then compare your response with the strong and weak answer patterns. Keep answers concrete:
name the user, data, baseline, metric, failure mode, and production plan.

## Core Preparation Checklist

- Clarify the role, user, decision, and constraints before naming a model.
- State assumptions about data availability, labels, latency, privacy, and cost.
- Start with a simple baseline and explain why added complexity is justified.
- Choose metrics that match the product decision and the cost of mistakes.
- Discuss leakage, drift, monitoring, rollback, and human review.
- Communicate tradeoffs in plain language and connect them to user impact.

## Interview Question Sections

### Question 1: Problem Framing and Baseline

**Question:** You are asked to design or analyze a solution involving {focus}. What would you clarify
first, and what baseline would you build before using a more complex approach?

**What the interviewer is testing:** Whether you can turn an ambiguous prompt into a measurable
engineering problem without hiding behind model names.

**Strong answer:** Clarify the user decision, available data, label or feedback source, constraints,
and failure cost. Propose a baseline that can be evaluated quickly, then state what evidence would
justify a more advanced model or architecture.

**Weak answer:** Jump straight to a model, skip the baseline, ignore data quality, and never define
how success will be measured.

**Follow-up questions:**

- What data would be available only after the decision is made?
- Which simple baseline would be hardest to beat?
- What metric would be misleading if used alone?

**Common traps:** Optimizing the offline metric without understanding the product decision, assuming
labels are clean, and ignoring high-risk segments.

### Question 2: Evaluation and Failure Modes

**Question:** How would you evaluate a system for {focus}, and how would you explain its most
important failure modes?

**What the interviewer is testing:** Whether you can connect metrics, error analysis, guardrails, and
production risk.

**Strong answer:** Define a primary metric, guardrail metrics, slice analysis, and a hard-example
set. Explain false positives, false negatives, latency or cost failures, privacy risks, and what
human review should handle.

**Weak answer:** Report one aggregate score and treat it as proof that the system is ready.

**Follow-up questions:**

- How would you detect a regression after release?
- Which segment would you inspect first?
- What would make the evaluation set untrustworthy?

**Common traps:** Confusing correlation with impact, overlooking delayed labels, and failing to
calibrate confidence.

### Question 3: Production Design and Communication

**Question:** How would you move a solution for {focus} from prototype to production, and how would
you explain the tradeoffs to a non-technical stakeholder?

**What the interviewer is testing:** Whether you understand ownership after launch.

**Strong answer:** Separate offline and online paths, version data and models, add monitoring and
rollback, define escalation, and explain tradeoffs between quality, latency, cost, privacy, and user
trust.

**Weak answer:** Stop at a notebook result or architecture sketch without deployment, monitoring, or
support plans.

**Follow-up questions:**

- What should be logged and what should not be logged?
- What happens when confidence is low?
- How would you roll back a bad release?

**Common traps:** Forgetting operational ownership, treating model output as always safe, and
communicating metrics without business context.

## Mini Exercise

Pick one project from this repository and give a five-minute answer using this structure: clarify,
baseline, data, metric, failure modes, production plan, and tradeoff summary. Rewrite the weakest
part until it is specific enough to defend.

## Diagram

```mermaid
flowchart LR
    A[Clarify] --> B[Baseline]
    B --> C[Data and model]
    C --> D[Evaluation]
    D --> E[Production controls]
    E --> F[Stakeholder explanation]
```
"""

def cheatsheet_body(path: Path) -> str:
    title = title_from_filename(path)
    topic = title.replace(" Cheatsheet", "")
    return f"""# {title}

## Intuition

{topic} is easiest to revise as a decision checklist. For any concept, ask what problem it solves,
what data or signal it needs, how it is evaluated, and what can fail in production.

## Explanation

Use this page as a fast reference for the ideas, metrics, traps, and answer structures connected to
{topic}. The goal is not to memorize isolated definitions. The goal is to move quickly from concept
to example, then from example to interview-ready reasoning.

## Why It Matters

Interviewers and real teams both look for the same signal: can you connect a technical idea to a
measurable decision, defend a baseline, and explain tradeoffs clearly. {topic} is useful only when it
helps you reason about data quality, model behavior, evaluation, cost, latency, or user impact.

## Example

If you are asked about {topic}, start with a concrete workflow such as search, recommendations,
fraud review, support routing, document retrieval, or model monitoring. Name the input, output,
baseline, metric, and one failure mode before adding detail.

## High-Yield Checklist

| Question | What a strong answer includes |
| --- | --- |
| What problem is being solved? | User, decision, input, output, and constraints |
| What is the baseline? | A simple measurable reference such as rules, majority class, linear model, lexical search, or retrieval |
| What metric matters? | A primary metric tied to the decision plus guardrails for safety, latency, cost, or fairness |
| What can go wrong? | Leakage, drift, bias, missing data, poor calibration, overfitting, or unsafe automation |
| What happens in production? | Monitoring, rollback, ownership, retraining triggers, and human escalation |

## Interview Angle

Use this answer shape: define the concept, give a small example, identify the baseline, choose the
metric, name the failure mode, and explain what you would monitor after launch.

## Common Mistakes

- Reciting definitions without a concrete user decision.
- Skipping the baseline and starting with a complex model.
- Reporting one metric without segment or failure analysis.
- Ignoring data leakage, drift, privacy, latency, cost, or rollback.
- Treating a polished demo as proof of production readiness.

## Mini Exercise

Explain {topic} in two minutes. Record the answer and check whether it included problem framing,
baseline, metric, failure mode, and production plan.

## Diagram

```mermaid
flowchart TD
    A[Frame problem] --> B[Choose baseline]
    B --> C[Evaluate]
    C --> D[Inspect failures]
    D --> E[Improve or simplify]
    E --> F[Monitor]
```
"""

def capstone_body(path: Path) -> str:
    title = title_from_filename(path)
    project_label = sentence_label(title)
    article = indefinite_article(project_label)
    domain, dataset, baseline, advanced, metric = CAPSTONE_DETAILS.get(
        content_slug(path),
        (project_label, "project-specific data and labels", "simple baseline", "improved model or retrieval system", "task quality and reliability"),
    )
    return f"""# {title}

## Goal

Build a focused {project_label} that demonstrates practical machine learning engineering: problem
framing, data handling, a measurable baseline, an improved approach, evaluation, communication, and
production thinking.

## Why This Project Matters

This project is useful because {domain} work forces you to connect model quality with user impact.
The strongest portfolio version shows not only a model score, but also data assumptions, error
analysis, monitoring needs, and the tradeoffs behind the final design.

## Intuition

Think of the project as a small production system. The model is one component. The surrounding work
defines the user decision, validates the data, compares against a baseline, measures failure modes,
and explains when the system should ask for human review.

## Explanation

Use {dataset}. Start with this baseline: {baseline}. Compare it with {advanced}. Keep the data split,
features, model version, and evaluation script easy to reproduce. Write down every assumption that
would change if the system had real users.

## Example Use Case

A realistic version of this project could help a team make a decision in {domain}. The system should
show the input, output, confidence or score, and one explanation of why the output is reasonable or
where it might fail.

## System Shape

```mermaid
flowchart LR
    A[Problem framing] --> B[Dataset]
    B --> C[Exploration]
    C --> D[Baseline]
    C --> E[Improved approach]
    D --> F[Evaluation report]
    E --> F
    F --> G[Demo or service]
    G --> H[Monitoring plan]
```

## Dataset Idea

Use {dataset}. If a public dataset is not available, create a small synthetic dataset that preserves
the structure of the real problem: inputs, labels or judgments, timestamps where useful, and edge
cases.

## Step-by-Step Implementation Plan

1. Write the product problem, target user, and success metric.
2. Create or collect the dataset and document each column or field.
3. Perform exploratory analysis and identify data quality risks.
4. Build the baseline: {baseline}.
5. Train or configure the improved approach: {advanced}.
6. Compare both approaches on the same split.
7. Analyze errors by segment and severity.
8. Package a small demo script, notebook, or API.
9. Add a model card style summary covering intended use, limits, risks, and monitoring.
10. Prepare a two-minute interview explanation.

## Evaluation

Use {metric}. Add guardrails for latency, cost, fairness or safety where relevant. Include examples
where the system succeeds, fails, and should defer to a human.

## Common Mistakes

- Starting with the advanced approach before measuring the baseline.
- Choosing a metric that does not match the user decision.
- Ignoring data leakage, missing values, drift, or delayed labels.
- Showing only aggregate results without segment analysis.
- Leaving out monitoring, rollback, privacy, or ownership.

## Resume Bullet Points

- Built {article} {project_label} with documented data pipeline, baseline, model comparison, and evaluation.
- Improved {metric} while adding error analysis and production risk assessment.
- Communicated tradeoffs using business impact, failure modes, and deployment constraints.

## Interview Angle

Start with the user problem, then describe the dataset, baseline, improved approach, metric, and
biggest lesson from error analysis. End with what you would do next if the project had real users.

## Mini Exercise

Write a one-page project proposal before coding. If you cannot define the metric, baseline, and
deployment path, simplify the project until you can.
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

def apply_interview_prep_cheatsheets_and_capstones() -> None:
    body_functions = {
        "interview-prep": interview_prep_body,
        "cheatsheets": cheatsheet_body,
        "capstone-projects": capstone_body,
    }
    for folder, body_function in body_functions.items():
        for path in learning_markdown_files(folder):
            existing_nav = navigation_block(path, ROOT / "README.md", ROOT / "README.md")
            text = read(path)
            marker = "\n---\n## Navigation\n"
            if marker in text:
                existing_nav = text[text.rfind(marker) + 1 :]
            write(path, body_function(path) + "\n\n" + existing_nav)

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
    apply_interview_prep_cheatsheets_and_capstones()
    apply_navigation()
    normalize_root_markdown_without_navigation()
    normalize_repository_text()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
