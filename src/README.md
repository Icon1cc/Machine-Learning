# Source Examples

This folder contains small educational Python examples that run locally without API keys. They are
designed to make the theory in the Markdown lessons concrete.

## Examples

- [ml_from_scratch/linear_regression.py](ml_from_scratch/linear_regression.py): batch gradient descent for linear regression.
- [ml_from_scratch/logistic_regression.py](ml_from_scratch/logistic_regression.py): binary classification with sigmoid loss.
- [ml_from_scratch/kmeans.py](ml_from_scratch/kmeans.py): clustering with centroid updates.
- [rag_demo/simple_rag_pipeline.py](rag_demo/simple_rag_pipeline.py): local bag-of-words retrieval plus answer synthesis.
- [agents_demo/simple_tool_agent.py](agents_demo/simple_tool_agent.py): deterministic tool-using agent loop.
- [mlops_demo/model_serving_example.py](mlops_demo/model_serving_example.py): minimal HTTP model serving example using the standard library.

## Running

Run examples from the repository root:

```bash
python src/ml_from_scratch/linear_regression.py
python src/rag_demo/simple_rag_pipeline.py
python src/agents_demo/simple_tool_agent.py
```

The examples avoid external services so they are suitable for offline study and interview practice.

---
## Navigation

[⬅ Previous](../capstone-projects/15-production-ml-platform.md) | [🏠 Home](../README.md) | [➡ Next](../diagrams/README.md)
