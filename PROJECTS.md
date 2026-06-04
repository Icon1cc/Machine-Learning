# Projects

Projects turn passive reading into durable skill. Each project should produce a clear README,
reproducible steps, a baseline, evaluation results, error analysis, and an interview-ready
explanation.

## Project Catalog

| Project | Domain | Baseline | Evaluation |
| --- | --- | --- | --- |
| [End-to-End Classical ML Project](capstone-projects/01-end-to-end-classical-ml-project.md) | tabular prediction | simple linear or tree baseline | F1, calibration, and segment performance |
| [House Price Prediction](capstone-projects/02-house-price-prediction.md) | real estate pricing | median-by-neighborhood baseline | MAE and error by price band |
| [Fraud Detection System](capstone-projects/03-fraud-detection-system.md) | transaction risk | rules plus logistic regression | fraud loss, false declines, and review precision |
| [Customer Churn Prediction](capstone-projects/04-customer-churn-prediction.md) | subscription retention | recency and usage rules | lift, calibration, and intervention cost |
| [Recommendation System](capstone-projects/05-recommendation-system.md) | personalized discovery | popular and recent items | CTR, conversion, diversity, and retention |
| [Search Ranking System](capstone-projects/06-search-ranking-system.md) | search relevance | BM25 with filters | NDCG, MRR, zero-result rate, and latency |
| [Image Classifier](capstone-projects/07-image-classifier.md) | image classification | simple CNN or transfer-learning baseline | accuracy, macro F1, and class-level recall |
| [NLP Text Classifier](capstone-projects/08-nlp-text-classifier.md) | text classification | TF-IDF linear model | macro F1, calibration, and per-class recall |
| [Semantic Search Engine](capstone-projects/09-semantic-search-engine.md) | semantic retrieval | BM25 search | recall at k, MRR, and p95 latency |
| [RAG Chatbot](capstone-projects/10-rag-chatbot.md) | grounded answering | keyword retrieval with snippets | faithfulness, citation precision, and latency |
| [Enterprise RAG Assistant](capstone-projects/11-enterprise-rag-assistant.md) | permission-aware knowledge access | permission-filtered search | answer quality, access correctness, and freshness |
| [LLM Evaluation Dashboard](capstone-projects/12-llm-evaluation-dashboard.md) | LLM release evaluation | golden test set checks | judge agreement, regression detection, and cost |
| [Agentic Research Assistant](capstone-projects/13-agentic-research-assistant.md) | research workflow support | retrieval plus structured notes | task success, citation accuracy, and unsafe action rate |
| [AI Customer Support Agent](capstone-projects/14-ai-customer-support-agent.md) | support automation | intent routing and templates | resolution rate, escalation accuracy, and safety incidents |
| [Production ML Platform](capstone-projects/15-production-ml-platform.md) | shared ML infrastructure | scripts and manual deployment checklist | reproducibility, deployment frequency, and incident rate |

## System Design Practice

Use these prompts when you want architecture practice rather than implementation practice.

| Prompt | Focus |
| --- | --- |
| [Design a Recommendation System](machine-learning-system-design/01-design-a-recommendation-system.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design a Search Ranking System](machine-learning-system-design/02-design-a-search-ranking-system.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design a Fraud Detection Platform](machine-learning-system-design/03-design-a-fraud-detection-platform.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design an ML Training Platform](machine-learning-system-design/04-design-an-ml-training-platform.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design a Feature Store](machine-learning-system-design/05-design-a-feature-store.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design a RAG Platform](machine-learning-system-design/06-design-a-rag-platform.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design an Agent Platform](machine-learning-system-design/07-design-an-agent-platform.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design an LLM Evaluation System](machine-learning-system-design/08-design-an-llm-evaluation-system.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design a Real Time Inference System](machine-learning-system-design/09-design-a-real-time-inference-system.md) | Requirements, data flow, serving, monitoring, and tradeoffs |
| [Design an AI Copilot Platform](machine-learning-system-design/10-design-an-ai-copilot-platform.md) | Requirements, data flow, serving, monitoring, and tradeoffs |

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
