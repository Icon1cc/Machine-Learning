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

FOLDER_INTUITION = {
    "fundamentals": "connect a business or product question to data, labels, models, metrics, and failure modes",
    "math": "turn geometry, rates of change, and information measures into tools for understanding model behavior",
    "statistics": "reason under uncertainty, measure evidence, and avoid drawing claims the data cannot support",
    "data-science": "turn messy records into evidence that supports a decision and can be explained to others",
    "classical-ml": "build strong, interpretable baselines for structured data before reaching for larger models",
    "deep-learning": "learn layered representations from tensors using gradients, architecture choices, and careful debugging",
    "nlp": "represent language so software can classify, extract, search, summarize, or generate text",
    "computer-vision": "treat images as tensors and learn spatial patterns that support visual decisions",
    "recommender-systems": "rank useful items for users while balancing relevance, diversity, freshness, and feedback loops",
    "mlops": "make machine learning reproducible, deployable, observable, and governable after the notebook stage",
    "generative-ai": "create useful new outputs while controlling quality, safety, provenance, and evaluation risk",
    "vector-databases": "retrieve semantically related items with embeddings, metadata, indexes, and ranking controls",
    "production-ai": "ship AI features that balance quality, latency, cost, privacy, safety, and ownership",
    "ethics-safety": "anticipate harms, privacy risks, misuse paths, and governance needs before release",
}

ROADMAP_PHASES = [
    ("0", "Setup and Learning Strategy", "Read the root README, choose a study plan, and set up Python examples.", "A realistic schedule and a clear definition of done for each study block."),
    ("1", "ML Foundations", "Study `fundamentals/` and practice framing inputs, labels, metrics, baselines, and splits.", "You can explain what makes a problem suitable for ML and what makes an evaluation misleading."),
    ("2", "Math for ML", "Study `math/` with emphasis on vectors, matrices, gradients, optimization, entropy, and distance.", "You can explain the math intuition behind loss minimization, similarity, PCA, and backpropagation."),
    ("3", "Statistics and Experimentation", "Study `statistics/` and connect uncertainty, sampling, hypothesis tests, and A/B tests to product decisions.", "You can reason about noisy evidence, confidence, leakage, bias, and causal claims."),
    ("4", "Data Science Workflow", "Study `data-science/` and practice cleaning, exploration, visualization, feature engineering, and communication.", "You can inspect a dataset, expose quality risks, and explain findings without overstating them."),
    ("5", "Classical ML", "Study `classical-ml/` and implement simple baselines before model selection.", "You can choose and compare linear models, trees, ensembles, clustering methods, and metrics."),
    ("6", "Deep Learning", "Study `deep-learning/` and trace forward propagation, backpropagation, optimizers, regularization, and transformers.", "You can debug training behavior and explain architecture tradeoffs clearly."),
    ("7", "Applied Modalities", "Study `nlp/`, `computer-vision/`, and `recommender-systems/`.", "You can map text, image, and ranking tasks to data, models, metrics, and failure modes."),
    ("8", "MLOps and Production AI", "Study `mlops/` and `production-ai/` together.", "You can describe reproducibility, serving, monitoring, rollback, latency, cost, privacy, and governance."),
    ("9", "Generative AI and LLMs", "Study `generative-ai/` and `llms/`.", "You can explain transformer-style generation, prompting, tuning choices, evaluation, guardrails, and serving constraints."),
    ("10", "Vector Search, RAG, and Agents", "Study `vector-databases/`, `rag/`, and `agents/`.", "You can design grounded assistants, retrieval pipelines, tool use, memory, observability, and risk controls."),
    ("11", "ML System Design", "Study `machine-learning-system-design/` and draw each architecture.", "You can walk through requirements, data flow, serving, scaling, evaluation, monitoring, and tradeoffs."),
    ("12", "Case Studies and Projects", "Study `case-studies/`, then build from `capstone-projects/`.", "You can turn concepts into a portfolio-quality project with evaluation and interview explanation."),
    ("13", "Interview Preparation", "Use `interview-prep/`, `mocks/`, `quizzes/`, and `cheatsheets/`.", "You can answer under time pressure with baseline, metric, failure mode, and production judgment."),
]

GLOSSARY_SECTIONS = {
    "ML Fundamentals": [
        ("Label", "The target value the model learns to predict. Bad labels create a ceiling on model quality."),
        ("Feature", "An input signal used by a model. Good features are available at prediction time and reflect the decision."),
        ("Dataset", "A collection of examples with inputs, metadata, labels, and provenance needed for learning or evaluation."),
        ("Training Set", "The examples used to fit model parameters."),
        ("Validation Set", "The examples used to choose models, thresholds, and hyperparameters before final testing."),
        ("Test Set", "A held-out set used for the final estimate of generalization."),
        ("Baseline", "The simplest measurable approach that a more complex model must beat."),
        ("Generalization", "Performance on new examples from the intended deployment distribution."),
        ("Overfitting", "Learning noise or quirks from training data that do not hold in deployment."),
        ("Underfitting", "Missing important structure because the model or features are too simple."),
        ("Data Leakage", "Using information during training or evaluation that would not be available at prediction time."),
        ("Calibration", "The degree to which predicted probabilities match observed frequencies."),
    ],
    "Math and Statistics": [
        ("Vector", "An ordered list of numbers that can represent features, embeddings, gradients, or parameters."),
        ("Matrix", "A rectangular array that represents linear transformations, batches, or model weights."),
        ("Dot Product", "A similarity and projection operation used in linear models, attention, and vector search."),
        ("Gradient", "The direction and rate of steepest increase for a function. Training usually moves against it."),
        ("Loss Function", "The objective a model minimizes during training."),
        ("Entropy", "A measure of uncertainty in a distribution."),
        ("Cross Entropy", "A loss used when comparing predicted probabilities with true classes."),
        ("KL Divergence", "A measure of how one probability distribution differs from another."),
        ("p-value", "A measure of how surprising the observed data would be under a null hypothesis."),
        ("Confidence Interval", "A range that describes uncertainty around an estimate."),
        ("Sampling Bias", "A mismatch between sampled data and the population or traffic you care about."),
        ("Causal Effect", "The change caused by an intervention, not just an association."),
    ],
    "Classical ML": [
        ("Linear Regression", "A model that predicts numeric values using a weighted sum of features."),
        ("Logistic Regression", "A linear classifier that outputs calibrated class probabilities when assumptions are reasonable."),
        ("Decision Tree", "A model that splits data with if-then rules."),
        ("Random Forest", "An ensemble of decision trees that reduces variance through averaging."),
        ("Gradient Boosting", "An ensemble that builds trees sequentially to correct previous errors."),
        ("SVM", "A margin-based classifier that can use kernels for non-linear boundaries."),
        ("Naive Bayes", "A probabilistic classifier with strong independence assumptions."),
        ("KNN", "A similarity-based method that predicts from nearby examples."),
        ("K-means", "A clustering method that assigns points to the nearest centroid."),
        ("DBSCAN", "A density-based clustering method that can find arbitrary shapes and noise."),
        ("PCA", "A dimensionality reduction method that finds directions of maximum variance."),
        ("SHAP", "An attribution method that estimates feature contribution to a prediction."),
    ],
    "Deep Learning and NLP": [
        ("Neuron", "A weighted transformation followed by a non-linear activation."),
        ("Activation Function", "A non-linearity that lets networks model complex relationships."),
        ("Backpropagation", "The algorithm that computes gradients through a computational graph."),
        ("Optimizer", "The update rule that changes parameters based on gradients."),
        ("Dropout", "A regularization method that randomly disables activations during training."),
        ("Batch Normalization", "A normalization layer that stabilizes training across mini-batches."),
        ("Attention", "A mechanism that weights relevant tokens, patches, or features for a given query."),
        ("Transformer", "An architecture built around attention, feed-forward layers, residual connections, and normalization."),
        ("Token", "A text unit processed by a model, often a word piece or byte-pair segment."),
        ("Embedding", "A dense vector representation of text, images, users, items, or documents."),
        ("NER", "Named entity recognition, which extracts entities such as people, products, locations, or dates."),
        ("Perplexity", "A language modeling metric related to how surprised the model is by text."),
    ],
    "LLMs, RAG, and Agents": [
        ("Context Window", "The maximum amount of text or tokens the model can consider in one request."),
        ("Instruction Tuning", "Training that makes a base model better at following user instructions."),
        ("RLHF", "Preference optimization using human feedback or preference models."),
        ("Hallucination", "A plausible output that is unsupported, false, or not grounded in available evidence."),
        ("Guardrail", "A control that constrains model behavior, validates output, or routes risky cases."),
        ("Chunk", "A document segment indexed for retrieval."),
        ("Retriever", "The component that finds candidate documents or chunks for a query."),
        ("Reranker", "A model that reorders retrieved candidates using richer relevance scoring."),
        ("Hybrid Search", "A retrieval strategy combining lexical and vector signals."),
        ("Faithfulness", "Whether an answer is supported by the retrieved evidence."),
        ("Agent Loop", "The observe, plan, act, and evaluate cycle used by a tool-using system."),
        ("Tool Schema", "The structured contract that tells an agent how to call an external capability."),
    ],
    "MLOps and Production AI": [
        ("Experiment Tracking", "Recording parameters, datasets, metrics, artifacts, and code versions for comparison."),
        ("Model Registry", "A controlled store for model versions, stages, metadata, and deployment approvals."),
        ("Feature Store", "A system for sharing, versioning, and serving features consistently offline and online."),
        ("Training-Serving Skew", "A mismatch between how features are produced during training and serving."),
        ("Batch Inference", "Predictions produced on a schedule for many examples at once."),
        ("Online Inference", "Predictions produced on demand for a live request."),
        ("Drift", "A change in data, labels, behavior, or relationships after deployment."),
        ("Canary Release", "A limited rollout used to compare a new version before broad release."),
        ("Shadow Deployment", "Running a model beside production without using its output for decisions."),
        ("Rollback", "Returning to a prior stable version after a bad release or incident."),
        ("SLO", "A target level for system behavior, such as latency or availability."),
        ("Audit Log", "A record of inputs, outputs, versions, and decisions needed for investigation."),
    ],
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

SYSTEM_DESIGN_DETAILS = {
    "design-a-recommendation-system": {
        "user": "a consumer app user opening a personalized home surface",
        "output": "a ranked list of items with diversity, freshness, and safety constraints",
        "baseline": "popular, recent, and followed-source candidates with simple engagement scoring",
        "advanced": "two-stage candidate generation and learning-to-rank with exploration and reranking",
        "data": "impressions, clicks, dwell time, hides, follows, item metadata, creator features, and freshness",
        "api": "GET /recommendations?user_id=&surface=&limit= returns ranked item ids, scores, reasons, and trace id",
        "metric": "NDCG, CTR, long-term retention, diversity, freshness, and negative feedback rate",
        "failure": "a feedback loop that over-optimizes short-term clicks and narrows discovery",
    },
    "design-a-search-ranking-system": {
        "user": "a user searching a product, document, or content corpus",
        "output": "ranked results with snippets, filters, scores, and trace metadata",
        "baseline": "BM25 with field boosts, query normalization, and permission or catalog filters",
        "advanced": "hybrid retrieval with vector search, learned ranking features, and reranking",
        "data": "queries, documents, metadata, clicks, skips, judgments, freshness, and permissions",
        "api": "GET /search?q=&filters=&user_id= returns ranked documents, snippets, facets, and trace id",
        "metric": "NDCG, MRR, zero-result rate, latency, abandonment, and judged relevance",
        "failure": "ranking stale, inaccessible, or semantically similar but wrong documents above the answer",
    },
    "design-a-fraud-detection-platform": {
        "user": "a payments or trust team deciding whether to approve, challenge, block, or review an event",
        "output": "risk score, action, reason codes, and review trace",
        "baseline": "velocity rules, deny lists, allow lists, and calibrated logistic regression",
        "advanced": "cost-sensitive gradient boosting with graph, device, and sequence features",
        "data": "transactions, account age, device, merchant, location, velocity, disputes, chargebacks, and review labels",
        "api": "POST /risk/score accepts event context and returns action, score, reason codes, and model version",
        "metric": "fraud loss prevented, false decline rate, review precision, chargeback rate, and p95 latency",
        "failure": "blocking legitimate high-value users or missing coordinated attacks because labels arrive late",
    },
    "design-an-ml-training-platform": {
        "user": "ML teams that need reproducible training, evaluation, model registration, and deployment handoff",
        "output": "versioned training runs, artifacts, metrics, lineage, and promotion decisions",
        "baseline": "scripted training jobs with manual experiment tracking and model artifact storage",
        "advanced": "orchestrated pipelines with dataset versioning, registry, approval gates, and scheduled retraining",
        "data": "datasets, feature snapshots, code versions, configs, metrics, artifacts, logs, and ownership metadata",
        "api": "POST /training-runs starts a run and GET /training-runs/{id} returns status, metrics, and artifacts",
        "metric": "reproducibility rate, training success rate, time to train, cost, and failed deployment rate",
        "failure": "a model cannot be reproduced or rolled back because data, code, or parameters were not versioned",
    },
    "design-a-feature-store": {
        "user": "ML teams sharing features between offline training and online inference",
        "output": "consistent offline datasets and low-latency online feature values",
        "baseline": "documented SQL transformations and batch materialized feature tables",
        "advanced": "managed feature registry with point-in-time joins, streaming updates, and online serving",
        "data": "raw events, entities, timestamps, transformation code, feature definitions, and freshness metadata",
        "api": "GET /features?entity_id=&feature_set= returns feature values, timestamps, and version metadata",
        "metric": "training-serving skew rate, feature freshness, p95 lookup latency, reuse, and incident count",
        "failure": "leaky point-in-time joins or stale online features create misleading model performance",
    },
    "design-a-rag-platform": {
        "user": "employees or customers asking questions over private and changing documents",
        "output": "grounded answer with citations, abstention, permissions, and trace id",
        "baseline": "permission-filtered keyword search with snippets and source links",
        "advanced": "hybrid retrieval, reranking, context compression, cite-or-abstain generation, and RAG evaluation",
        "data": "documents, chunks, ACLs, metadata, embeddings, queries, answers, citations, and feedback",
        "api": "POST /rag/query accepts question and user context and returns answer, citations, abstention, and trace id",
        "metric": "retrieval recall, context precision, faithfulness, citation accuracy, p95 latency, and access violations",
        "failure": "retrieving restricted or stale content, or generating an unsupported answer with confident wording",
    },
    "design-an-agent-platform": {
        "user": "teams building tool-using assistants for bounded operational workflows",
        "output": "task result, tool trace, approval requests, state transitions, and audit log",
        "baseline": "deterministic workflow automation with forms, rules, and manual approval steps",
        "advanced": "bounded agent loop with tool schemas, state store, policy checks, memory, and human checkpoints",
        "data": "user goals, tool schemas, permissions, task state, documents, observations, and feedback",
        "api": "POST /agent/tasks starts a task and GET /agent/tasks/{id} returns state, actions, and approvals",
        "metric": "task success, unsafe action rate, approval rate, intervention rate, latency, and audit completeness",
        "failure": "the agent changes external state without permission or repeats tool calls after partial failure",
    },
    "design-an-llm-evaluation-system": {
        "user": "product and ML teams deciding whether an LLM workflow is safe enough to release",
        "output": "scorecards, regressions, trace failures, review queues, and release recommendation",
        "baseline": "golden datasets with deterministic checks and human-reviewed release notes",
        "advanced": "calibrated LLM judges, pairwise comparison, trace-level diagnostics, and slice dashboards",
        "data": "prompts, outputs, rubrics, traces, citations, tool calls, judge versions, human labels, and costs",
        "api": "POST /eval/runs starts an evaluation and GET /eval/runs/{id} returns scorecards and failures",
        "metric": "regression detection, judge agreement, coverage, false alarm rate, review load, latency, and cost",
        "failure": "a fluent but unsupported output passes because the judge or dataset missed the workflow risk",
    },
    "design-a-real-time-inference-system": {
        "user": "a product surface that needs low-latency model predictions during live requests",
        "output": "prediction, confidence, model version, feature version, and fallback decision",
        "baseline": "single model endpoint with cached features and a rules fallback",
        "advanced": "autoscaled serving, batching, model routing, feature cache, canary release, and observability",
        "data": "online features, request context, model artifacts, prediction logs, labels, latency, and errors",
        "api": "POST /predict accepts request context and returns prediction, confidence, versions, and trace id",
        "metric": "p95 latency, timeout rate, throughput, cost per prediction, model quality, and fallback rate",
        "failure": "feature lookup or model latency exceeds budget and silently changes product behavior",
    },
    "design-an-ai-copilot-platform": {
        "user": "knowledge workers using an AI assistant inside an existing product workflow",
        "output": "draft, recommendation, tool action, or explanation with citations and approval state",
        "baseline": "retrieval-backed suggestions with templates and human confirmation",
        "advanced": "context orchestration, tool use, permissions, policy checks, evaluation, and feedback learning",
        "data": "user context, documents, UI state, permissions, tool results, prompts, traces, and feedback",
        "api": "POST /copilot/actions accepts context and intent and returns suggestion, evidence, tools, and trace id",
        "metric": "task completion, acceptance rate, edit rate, groundedness, unsafe action rate, latency, and cost",
        "failure": "the assistant suggests or performs an action outside user intent, policy, or permissions",
    },
}

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
    title = " ".join(words).replace("End To End", "End-to-End")
    return title.replace(" A ", " a ").replace(" An ", " an ").replace(" The ", " the ")

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
    if lower_label.startswith(("ai", "end-to-end", "enterprise", "image", "llm", "ml", "nlp")):
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

## Repository Index

Use [REPO_INDEX.md](REPO_INDEX.md) when you want a single grouped list of every Markdown file in
the repository. Regenerate it after adding, renaming, or removing learning material.

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

def roadmap_doc() -> str:
    rows = [
        f"| {number} | {name} | {focus} | {outcome} |"
        for number, name, focus, outcome in ROADMAP_PHASES
    ]
    phases = []
    for number, name, focus, outcome in ROADMAP_PHASES:
        phases.append(
            f"""## Phase {number}. {name}

**Focus:** {focus}

**Practice:** Write one concrete example, one failure mode, one interview question, and one metric
for this phase before moving on.

**Expected outcome:** {outcome}
"""
        )
    return f"""# Roadmap

This roadmap keeps the repository practical. Move from foundations to implementation, then to
production systems, case studies, projects, and interviews. Each phase should end with something you
can explain out loud.

## Summary

| Phase | Area | Focus | Outcome |
| --- | --- | --- | --- |
{chr(10).join(rows)}

## How to Use This Roadmap

1. Read the listed folders in order.
2. Complete the mini exercises inside each lesson.
3. Use one quiz or cheatsheet for retrieval practice.
4. Build or sketch one small artifact before advancing.
5. Explain the phase using baseline, metric, failure mode, and production tradeoff.

{chr(10).join(phases)}
## Roadmap Diagram

```mermaid
flowchart TD
    A[Foundations] --> B[Math and Statistics]
    B --> C[Data and Classical ML]
    C --> D[Deep Learning and Modalities]
    D --> E[MLOps and Production AI]
    E --> F[LLMs, RAG, and Agents]
    F --> G[ML System Design]
    G --> H[Case Studies and Projects]
    H --> I[Interview Preparation]
```
"""

def study_plan_doc() -> str:
    twelve_week = [
        ("1", "Foundations", "`fundamentals/`", "Frame one product problem with input, label, metric, and baseline."),
        ("2", "Math", "`math/`", "Explain gradients, matrix multiplication, and similarity with one worked example."),
        ("3", "Statistics", "`statistics/`", "Design an A/B test and list leakage or sampling risks."),
        ("4", "Data Science", "`data-science/`", "Clean a small dataset and write an EDA memo."),
        ("5", "Classical ML", "`classical-ml/`", "Train a baseline and compare two metrics."),
        ("6", "Deep Learning", "`deep-learning/`", "Trace a forward pass and debug one training failure."),
        ("7", "NLP, Vision, Recommenders", "`nlp/`, `computer-vision/`, `recommender-systems/`", "Map each modality to its data, metric, and common failure."),
        ("8", "MLOps and Production AI", "`mlops/`, `production-ai/`", "Draw a serving and monitoring plan."),
        ("9", "Generative AI and LLMs", "`generative-ai/`, `llms/`", "Compare prompting, RAG, and fine-tuning for one use case."),
        ("10", "Vector Search, RAG, Agents", "`vector-databases/`, `rag/`, `agents/`", "Design a grounded assistant with permissions and evaluation."),
        ("11", "ML System Design and Case Studies", "`machine-learning-system-design/`, `case-studies/`", "Complete two architecture walkthroughs."),
        ("12", "Projects and Interviews", "`capstone-projects/`, `interview-prep/`, `mocks/`", "Finish one project plan and run two mock rounds."),
    ]
    twenty_four_rows = []
    for week, topic, files, outcome in twelve_week:
        first = int(week) * 2 - 1
        second = first + 1
        twenty_four_rows.append((str(first), topic, files, "Read, summarize, and answer one quiz."))
        twenty_four_rows.append((str(second), topic, files, outcome))
    six_week = [
        ("1", "Core ML", "`fundamentals/`, `math/`, `statistics/`", "Explain splits, leakage, metrics, and uncertainty."),
        ("2", "Data and Classical ML", "`data-science/`, `classical-ml/`", "Defend a baseline and compare model families."),
        ("3", "Deep Learning and Modalities", "`deep-learning/`, `nlp/`, `computer-vision/`, `recommender-systems/`", "Explain architectures and task metrics."),
        ("4", "Production and LLM Systems", "`mlops/`, `production-ai/`, `llms/`, `rag/`, `agents/`", "Discuss latency, cost, monitoring, safety, and evaluation."),
        ("5", "System Design", "`machine-learning-system-design/`, `case-studies/`", "Complete three whiteboard-style designs."),
        ("6", "Mocks and Final Review", "`interview-prep/`, `mocks/`, `cheatsheets/`", "Run timed mocks and repair weak answers."),
    ]

    def table(rows: list[tuple[str, str, str, str]]) -> str:
        lines = ["| Week | Topics | Files | Outcome |", "| --- | --- | --- | --- |"]
        lines.extend(f"| {week} | {topic} | {files} | {outcome} |" for week, topic, files, outcome in rows)
        return "\n".join(lines)

    return f"""# Study Plan

Use these plans as schedules, not rules. Keep the order when possible, but slow down when a topic
needs more practice. Every week should produce a visible artifact: notes, a diagram, a baseline, an
evaluation, a case-study walkthrough, or a mock interview review.

## 12-Week Focused Plan

{table(twelve_week)}

## 24-Week Balanced Plan

{table(twenty_four_rows)}

## 6-Week Interview Revision Plan

{table(six_week)}

## Weekly Routine

| Activity | Time | Output |
| --- | --- | --- |
| Reading | 2 to 4 sessions | Five-bullet summary per file |
| Practice | 1 to 2 sessions | Quiz answers, exercises, or notebook edits |
| Build or design | 1 session | Baseline, diagram, or project note |
| Interview rehearsal | 1 session | Spoken answer with feedback notes |
| Review | 30 minutes | Updated weak-topic list |

## Project-First Route

1. Choose one guide from [capstone-projects/](capstone-projects/) or one prompt from [machine-learning-system-design/](machine-learning-system-design/).
2. Read only the files needed for the next implementation or design step.
3. Build a baseline before adding model complexity.
4. Add evaluation before optimizing.
5. Keep a project journal with data choices, failed experiments, and tradeoffs.
6. Turn the final writeup into resume bullets and interview stories.

## Diagram

```mermaid
flowchart LR
    Read --> Recall
    Recall --> Build
    Build --> Evaluate
    Evaluate --> Explain
    Explain --> Review
    Review --> Read
```
"""

def interview_guide_doc() -> str:
    return """# Interview Guide

## What Interviewers Are Testing

AI and ML interviews test whether you can turn uncertain data problems into useful systems. A strong
answer moves from product framing to data, baseline, model choice, evaluation, failure modes, and
production operations. Formulas matter, but they are not enough without assumptions and tradeoffs.

## Core Answer Framework

| Step | What to say |
| --- | --- |
| Clarify | User, decision, scope, constraints, and cost of mistakes |
| Data | Inputs, labels, feedback, freshness, permissions, and leakage risks |
| Baseline | The simplest measurable approach and why it is a fair reference |
| Model or design | The chosen method, why it fits, and what complexity it adds |
| Evaluation | Primary metric, guardrails, slices, regression set, and error analysis |
| Production | Serving path, latency, cost, monitoring, rollback, privacy, and ownership |

## Strong Answer Pattern

1. State the goal in one sentence.
2. Define input, output, and metric.
3. Start with a baseline.
4. Add the model or architecture only after naming the failure the baseline cannot handle.
5. Evaluate with slices and hard examples.
6. Discuss deployment constraints and rollback.
7. End with the biggest tradeoff.

## Common Interview Areas

| Area | High-signal topics |
| --- | --- |
| Fundamentals | Splits, leakage, baselines, bias-variance, metrics, and generalization |
| Statistics | A/B tests, uncertainty, sampling bias, causality, and experiment design |
| Classical ML | Linear models, trees, ensembles, clustering, calibration, and interpretability |
| Deep Learning | Backpropagation, optimization, regularization, transformers, and debugging |
| LLM Systems | Prompting, RAG, vector search, agents, guardrails, evaluation, and serving |
| System Design | Offline-online paths, data flow, monitoring, scaling, reliability, and cost |
| Behavioral | Ownership, ambiguity, debugging, stakeholder communication, and impact |

## Traps to Avoid

- Starting with a model name before clarifying the decision.
- Reporting one aggregate metric without segment analysis.
- Ignoring leakage, delayed labels, drift, or feedback loops.
- Treating offline performance as production readiness.
- Forgetting privacy, authorization, audit logs, rollback, and human review.

## Practice Plan

Use [interview-prep/](interview-prep/) for question drills, [machine-learning-system-design/](machine-learning-system-design/)
for architecture practice, [mocks/](mocks/) for full rounds, and [cheatsheets/](cheatsheets/) for
quick revision. After every mock, rewrite one answer using the framework above.

## Diagram

```mermaid
flowchart TD
    A[Clarify] --> B[Data]
    B --> C[Baseline]
    C --> D[Model or design]
    D --> E[Evaluation]
    E --> F[Production plan]
    F --> G[Tradeoff summary]
```
"""

def projects_doc() -> str:
    capstone_rows = []
    for path in learning_markdown_files("capstone-projects"):
        details = CAPSTONE_DETAILS.get(content_slug(path), ("project work", "data", "baseline", "advanced", "metric"))
        capstone_rows.append(f"| [{title_from_filename(path)}]({path.relative_to(ROOT).as_posix()}) | {details[0]} | {details[2]} | {details[4]} |")
    design_rows = []
    for path in learning_markdown_files("machine-learning-system-design"):
        design_rows.append(f"| [{title_from_filename(path)}]({path.relative_to(ROOT).as_posix()}) | Requirements, data flow, serving, monitoring, and tradeoffs |")
    return f"""# Projects

Projects turn passive reading into durable skill. Each project should produce a clear README,
reproducible steps, a baseline, evaluation results, error analysis, and an interview-ready
explanation.

## Project Catalog

| Project | Domain | Baseline | Evaluation |
| --- | --- | --- | --- |
{chr(10).join(capstone_rows)}

## System Design Practice

Use these prompts when you want architecture practice rather than implementation practice.

| Prompt | Focus |
| --- | --- |
{chr(10).join(design_rows)}

## Project Quality Bar

- A baseline is implemented before advanced modeling.
- Data assumptions and limitations are documented.
- Evaluation includes more than one aggregate score.
- Failure cases are shown honestly.
- The project includes a short monitoring and rollback plan.
- The project can be explained in two minutes and defended for twenty minutes.

## Recommended Portfolio Sequence

1. Build one tabular classical ML project.
2. Build one retrieval or RAG project.
3. Build one production or MLOps project.
4. Write one system design walkthrough.
5. Convert the strongest project into resume bullets and a mock interview story.

## Diagram

```mermaid
flowchart LR
    Idea --> Dataset
    Dataset --> Baseline
    Baseline --> Improved_Model[Improved model]
    Improved_Model --> Evaluation
    Evaluation --> Error_Analysis[Error analysis]
    Error_Analysis --> Writeup
    Writeup --> Interview
```
"""

def glossary_doc() -> str:
    sections = []
    for section, terms in GLOSSARY_SECTIONS.items():
        rows = ["| Term | Meaning |", "| --- | --- |"]
        rows.extend(f"| {term} | {definition} |" for term, definition in terms)
        sections.append(f"## {section}\n\n" + "\n".join(rows) + "\n")
    return f"""# Glossary

This glossary defines high-yield terms used across the repository. Use it for quick recall, then
return to the lessons, cheatsheets, and case studies for deeper practice.

## How to Use This Glossary

- Review one category before starting the matching folder.
- Convert each definition into a concrete example.
- During interview prep, explain the term with input, output, metric, and failure mode where relevant.

{chr(10).join(sections)}

## Revision Checklist

- [ ] I can define each term in plain language.
- [ ] I can give one example for each major category.
- [ ] I can name one common mistake or failure mode for the production-facing terms.
- [ ] I can connect glossary terms back to a project or case study.
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

## What to Know Before Starting

- Read the previous folder in the root recommended order when possible.
- Know the user problem, input data, output, metric, and one common failure mode for the topic.
- Keep a small notes file with definitions, examples, and questions that remain unclear.

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

## Practice Guidance

For each lesson, write a concrete example before reviewing the interview angle. If the topic has a
model, retrieval, serving, or evaluation component, identify the simplest baseline and the most
likely production failure. End the section by explaining the tradeoff out loud in two minutes.

## Navigation

[🏠 Home](../README.md)
"""

def normalize_text(text: str) -> str:
    text = text.replace("\u2014", "-")
    text = text.replace("What Is a ", "What Is a ")
    text = text.replace("What Is an ", "What Is an ")
    text = text.replace("Design a ", "Design a ")
    text = text.replace("Design an ", "Design an ")
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
    title_label = sentence_label(title)
    article = indefinite_article(title_label)
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

Build {article} {title_label} for {domain}. The system uses {inputs} to support this output:
{output}. Treat the case as an interview design exercise and a production review: define the
decision, start with a baseline, measure quality honestly, and explain how the system behaves when
confidence is low.

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

## Data Assumptions

- Inputs are timestamped so training, validation, and serving windows can be separated.
- Sensitive fields are minimized, redacted, or access-controlled before modeling.
- Labels or judgments have known delay, noise, and reviewer disagreement.
- Feedback can be joined back to model versions, prompts, features, or retrieval indexes.

## Architecture Diagram

```mermaid
flowchart LR
    A[Product request] --> B[Input validation]
    B --> C[Feature, chunk, or context pipeline]
    C --> D[Baseline]
    C --> E[Advanced approach]
    D --> F[Offline evaluation]
    E --> F
    F --> G[Serving or workflow layer]
    G --> H[Monitoring, feedback, and review]
    H --> C
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

## Model Choices

| Option | When it fits | Main risk |
| --- | --- | --- |
| Rules or search baseline | The workflow needs explainability and fast iteration | Can miss nuanced patterns |
| Classical model | Tabular or sparse features carry strong signal | Can leak features or underfit complex behavior |
| Deep model or LLM workflow | Text, images, retrieval, or reasoning dominate the task | Higher latency, cost, and evaluation burden |
| Human review | Errors are costly or confidence is low | Review capacity can become the bottleneck |

## Evaluation Plan

Evaluate with {metric}. Include slice analysis for important user, item, time, source, language, or
risk segments. Keep a small set of hard examples for regression checks and review disagreements
between model outputs and human judgment.

## Metrics and Guardrails

| Metric Type | Examples |
| --- | --- |
| Primary quality | {metric} |
| Guardrail | Latency, cost, privacy incidents, unsafe actions, and user complaints |
| Data quality | Missing fields, stale inputs, label delay, and source coverage |
| Operations | Error rate, timeout rate, review backlog, rollback count, and alert response time |

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

## Failure Modes

- The system optimizes an offline metric that does not match the product decision.
- Feedback loops reinforce early mistakes or popular items.
- A data pipeline change silently shifts feature values or retrieval quality.
- Confidence is poorly calibrated, causing the system to automate cases that need review.
- The critical failure to plan around is {failure}.

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
    details = SYSTEM_DESIGN_DETAILS.get(content_slug(path), {})
    user = details.get("user", "a product team using machine learning in a live workflow")
    output = details.get("output", "a useful prediction, ranking, answer, or action")
    baseline = details.get("baseline", "a simple measurable baseline")
    advanced = details.get("advanced", "a more capable architecture with explicit controls")
    data = details.get("data", "events, features, labels, metadata, model versions, logs, and feedback")
    api = details.get("api", "a minimal API that returns output, confidence, versions, and trace id")
    metric = details.get("metric", "task quality, latency, cost, reliability, and user impact")
    failure = details.get("failure", "a production behavior that is not covered by offline evaluation")
    return f"""# {title}

## Beginner-Friendly Intuition

{title} is about designing a reliable workflow for {user}. The model is only one part of the design.
The system must collect trustworthy data, produce the expected output ({output}), serve it within
constraints, monitor quality, handle failures, and give the team a way to improve or roll back.

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
| Data | What data is available, fresh, reliable, permitted, and logged? |
| Baseline | What simple design creates the first measurable reference point? |
| Serving | Is the system batch, online, streaming, or hybrid? |
| Operations | How are drift, failures, cost, and latency monitored? |

## Requirements to Clarify

- User and decision: {user}.
- Expected output: {output}.
- Latency, throughput, freshness, privacy, and cost constraints.
- Error cost, human review policy, and rollback expectations.
- Data access rules, audit requirements, and abuse cases.

## Capacity and Data Assumptions

- Start with realistic traffic and latency assumptions, then state how the design scales.
- Data includes {data}.
- Labels or feedback may be delayed, biased by what the system showed, or missing for rare failures.
- Offline training data must be separated from online serving data by time and availability.

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

## API Contract

{api}.

The response should include enough metadata to debug production behavior: model or index version,
feature or prompt version, latency, fallback status, and trace id.

## Data and Feature Design

Store raw events separately from derived features, chunks, rankings, predictions, traces, and labels.
Version every artifact that can change. For online systems, enforce point-in-time correctness so the
training path does not use information that would not exist at serving time.

## Baseline and Advanced Design

| Layer | First version | Stronger version |
| --- | --- | --- |
| Decision logic | {baseline} | {advanced} |
| Evaluation | Offline metric and hand-inspected failures | Slices, hard examples, online tests, and guardrails |
| Operations | Logs and simple alerts | Versioned rollouts, drift monitoring, ownership, and rollback |

## Real-World Example

A realistic first version would ship {baseline}. The team would measure {metric}, inspect failures,
and only then move toward {advanced}. This keeps the design honest: model complexity is justified by
a measured miss, not by preference for a sophisticated architecture.

## Scaling, Reliability, and Cost

- Separate offline computation from online serving where possible.
- Cache stable features, embeddings, candidates, or responses when freshness allows.
- Use canaries, shadow traffic, and rollback for risky releases.
- Define fallback behavior for missing features, model timeouts, provider errors, and low confidence.
- Track cost per request, expensive dependencies, and the point where batching or precomputation pays off.

## Observability and Security

- Log inputs, versions, outputs, latency, fallback status, and user feedback with privacy controls.
- Monitor {metric} plus technical health such as error rate, queue depth, and p95 latency.
- Enforce authorization before retrieval, scoring, or tool action when sensitive data is involved.
- Redact private data, limit retention, and make audit trails available for high-impact decisions.

## Bottlenecks and Failure Modes

The primary failure to plan around is {failure}. Other common bottlenecks include delayed labels,
feature freshness, expensive inference, unowned alerts, biased feedback, and silent data pipeline
changes.

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
- How would you defend the design if traffic or data volume increased ten times?

## Mini Exercise

Draw the first version of this system on one page. Include data sources, feature or embedding
generation, model or retrieval path, serving layer, monitoring, and human review. Then write one
paragraph explaining the biggest tradeoff.

## Diagram

```mermaid
flowchart LR
    A[User workflow] --> B[Data and context]
    B --> C[Baseline]
    B --> D[Advanced design]
    C --> E[Evaluation and guardrails]
    D --> E
    E --> F[Serving layer]
    F --> G[Logs, feedback, monitoring]
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

Build a focused {project_label} with a clear problem statement, reproducible data path, measurable
baseline, improved approach, evaluation report, and interview-ready explanation.

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

## Architecture

Keep the first implementation small. Use a data preparation layer, one baseline, one improved
approach, one evaluation script, and a thin demo or service. Record artifact versions so results can
be reproduced later.

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

## Evaluation Strategy

- Compare the baseline and improved approach on the same split.
- Include at least three representative success cases and three failure cases.
- Report segment-level results, not only one aggregate metric.
- Add a small regression set that protects the most important behavior.

## Extensions

- Add monitoring for data drift, latency, cost, and quality regressions.
- Add a human review path for low-confidence or high-risk outputs.
- Package the result as a CLI, notebook, small API, or dashboard.
- Write a short model card or system card covering intended use and limits.

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

def topic_intuition_body(path: Path) -> str:
    title = title_from_filename(path)
    folder = path.parent.name
    focus = FOLDER_INTUITION.get(
        folder,
        "connect the concept to a concrete decision, measurable evidence, and a failure mode",
    )
    return f"""## Beginner-Friendly Intuition

{title} is best learned as a practical lever, not as an isolated definition. In this part of the
curriculum, the goal is to {focus}. Start by asking what input changes, what output or decision
improves, and what mistake becomes easier to catch.

For a beginner, a useful test is simple: explain the concept with one realistic workflow, one
baseline, one metric, and one failure mode. If those four pieces are clear, the formal details have
a place to attach.
"""

def replace_section(text: str, heading: str, replacement: str, next_heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return text
    end = text.find(next_heading, start + len(heading))
    if end == -1:
        return text
    return text[:start].rstrip() + "\n\n" + replacement.rstrip() + "\n\n" + text[end:].lstrip()

def apply_topic_intuition_refresh() -> None:
    for folder in FOLDER_INTUITION:
        for path in learning_markdown_files(folder):
            text = read(path)
            if "recurring goal" not in text and "plain workflow" not in text:
                continue
            updated = replace_section(
                text,
                "## Beginner-Friendly Intuition",
                topic_intuition_body(path),
                "## Formal Explanation",
            )
            write(path, updated)

def apply_root_learning_docs() -> None:
    write(ROOT / "ROADMAP.md", roadmap_doc())
    write(ROOT / "STUDY_PLAN.md", study_plan_doc())
    write(ROOT / "INTERVIEW_GUIDE.md", interview_guide_doc())
    write(ROOT / "PROJECTS.md", projects_doc())
    write(ROOT / "GLOSSARY.md", glossary_doc())

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

def apply_interview_prep_cheatsheets_and_capstones() -> None:
    body_functions = {
        "interview-prep": interview_prep_body,
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
    apply_root_learning_docs()
    apply_folder_readmes()
    apply_topic_intuition_refresh()
    apply_case_studies_and_mocks()
    apply_interview_prep_cheatsheets_and_capstones()
    apply_navigation()
    normalize_root_markdown_without_navigation()
    normalize_repository_text()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
