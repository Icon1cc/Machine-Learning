# Glossary

This glossary defines high-yield terms used across the repository. Use it for quick recall, then
return to the lessons, cheatsheets, and case studies for deeper practice.

## How to Use This Glossary

- Review one category before starting the matching folder.
- Convert each definition into a concrete example.
- During interview prep, explain the term with input, output, metric, and failure mode where relevant.

## ML Fundamentals

| Term | Meaning |
| --- | --- |
| Label | The target value the model learns to predict. Bad labels create a ceiling on model quality. |
| Feature | An input signal used by a model. Good features are available at prediction time and reflect the decision. |
| Dataset | A collection of examples with inputs, metadata, labels, and provenance needed for learning or evaluation. |
| Training Set | The examples used to fit model parameters. |
| Validation Set | The examples used to choose models, thresholds, and hyperparameters before final testing. |
| Test Set | A held-out set used for the final estimate of generalization. |
| Baseline | The simplest measurable approach that a more complex model must beat. |
| Generalization | Performance on new examples from the intended deployment distribution. |
| Overfitting | Learning noise or quirks from training data that do not hold in deployment. |
| Underfitting | Missing important structure because the model or features are too simple. |
| Data Leakage | Using information during training or evaluation that would not be available at prediction time. |
| Calibration | The degree to which predicted probabilities match observed frequencies. |

## Math and Statistics

| Term | Meaning |
| --- | --- |
| Vector | An ordered list of numbers that can represent features, embeddings, gradients, or parameters. |
| Matrix | A rectangular array that represents linear transformations, batches, or model weights. |
| Dot Product | A similarity and projection operation used in linear models, attention, and vector search. |
| Gradient | The direction and rate of steepest increase for a function. Training usually moves against it. |
| Loss Function | The objective a model minimizes during training. |
| Entropy | A measure of uncertainty in a distribution. |
| Cross Entropy | A loss used when comparing predicted probabilities with true classes. |
| KL Divergence | A measure of how one probability distribution differs from another. |
| p-value | A measure of how surprising the observed data would be under a null hypothesis. |
| Confidence Interval | A range that describes uncertainty around an estimate. |
| Sampling Bias | A mismatch between sampled data and the population or traffic you care about. |
| Causal Effect | The change caused by an intervention, not just an association. |

## Classical ML

| Term | Meaning |
| --- | --- |
| Linear Regression | A model that predicts numeric values using a weighted sum of features. |
| Logistic Regression | A linear classifier that outputs calibrated class probabilities when assumptions are reasonable. |
| Decision Tree | A model that splits data with if-then rules. |
| Random Forest | An ensemble of decision trees that reduces variance through averaging. |
| Gradient Boosting | An ensemble that builds trees sequentially to correct previous errors. |
| SVM | A margin-based classifier that can use kernels for non-linear boundaries. |
| Naive Bayes | A probabilistic classifier with strong independence assumptions. |
| KNN | A similarity-based method that predicts from nearby examples. |
| K-means | A clustering method that assigns points to the nearest centroid. |
| DBSCAN | A density-based clustering method that can find arbitrary shapes and noise. |
| PCA | A dimensionality reduction method that finds directions of maximum variance. |
| SHAP | An attribution method that estimates feature contribution to a prediction. |

## Deep Learning and NLP

| Term | Meaning |
| --- | --- |
| Neuron | A weighted transformation followed by a non-linear activation. |
| Activation Function | A non-linearity that lets networks model complex relationships. |
| Backpropagation | The algorithm that computes gradients through a computational graph. |
| Optimizer | The update rule that changes parameters based on gradients. |
| Dropout | A regularization method that randomly disables activations during training. |
| Batch Normalization | A normalization layer that stabilizes training across mini-batches. |
| Attention | A mechanism that weights relevant tokens, patches, or features for a given query. |
| Transformer | An architecture built around attention, feed-forward layers, residual connections, and normalization. |
| Token | A text unit processed by a model, often a word piece or byte-pair segment. |
| Embedding | A dense vector representation of text, images, users, items, or documents. |
| NER | Named entity recognition, which extracts entities such as people, products, locations, or dates. |
| Perplexity | A language modeling metric related to how surprised the model is by text. |

## LLMs, RAG, and Agents

| Term | Meaning |
| --- | --- |
| Context Window | The maximum amount of text or tokens the model can consider in one request. |
| Instruction Tuning | Training that makes a base model better at following user instructions. |
| RLHF | Preference optimization using human feedback or preference models. |
| Hallucination | A plausible output that is unsupported, false, or not grounded in available evidence. |
| Guardrail | A control that constrains model behavior, validates output, or routes risky cases. |
| Chunk | A document segment indexed for retrieval. |
| Retriever | The component that finds candidate documents or chunks for a query. |
| Reranker | A model that reorders retrieved candidates using richer relevance scoring. |
| Hybrid Search | A retrieval strategy combining lexical and vector signals. |
| Faithfulness | Whether an answer is supported by the retrieved evidence. |
| Agent Loop | The observe, plan, act, and evaluate cycle used by a tool-using system. |
| Tool Schema | The structured contract that tells an agent how to call an external capability. |

## MLOps and Production AI

| Term | Meaning |
| --- | --- |
| Experiment Tracking | Recording parameters, datasets, metrics, artifacts, and code versions for comparison. |
| Model Registry | A controlled store for model versions, stages, metadata, and deployment approvals. |
| Feature Store | A system for sharing, versioning, and serving features consistently offline and online. |
| Training-Serving Skew | A mismatch between how features are produced during training and serving. |
| Batch Inference | Predictions produced on a schedule for many examples at once. |
| Online Inference | Predictions produced on demand for a live request. |
| Drift | A change in data, labels, behavior, or relationships after deployment. |
| Canary Release | A limited rollout used to compare a new version before broad release. |
| Shadow Deployment | Running a model beside production without using its output for decisions. |
| Rollback | Returning to a prior stable version after a bad release or incident. |
| SLO | A target level for system behavior, such as latency or availability. |
| Audit Log | A record of inputs, outputs, versions, and decisions needed for investigation. |

## Revision Checklist

- [ ] I can define each term in plain language.
- [ ] I can give one example for each major category.
- [ ] I can name one common mistake or failure mode for the production-facing terms.
- [ ] I can connect glossary terms back to a project or case study.
