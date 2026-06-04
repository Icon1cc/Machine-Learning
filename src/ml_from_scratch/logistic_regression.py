"""Educational binary logistic regression implemented with NumPy."""

from __future__ import annotations

import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


class LogisticRegressionGD:
    """Fit a binary classifier by minimizing cross-entropy."""

    def __init__(self, learning_rate: float = 0.1, epochs: int = 1000) -> None:
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights: np.ndarray | None = None
        self.bias = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> "LogisticRegressionGD":
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        self.weights = np.zeros(x.shape[1])
        self.bias = 0.0

        for _ in range(self.epochs):
            probabilities = sigmoid(x @ self.weights + self.bias)
            errors = probabilities - y
            self.weights -= self.learning_rate * (x.T @ errors / len(x))
            self.bias -= self.learning_rate * errors.mean()
        return self

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        if self.weights is None:
            raise RuntimeError("Model must be fitted before prediction.")
        return sigmoid(np.asarray(x, dtype=float) @ self.weights + self.bias)

    def predict(self, x: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(x) >= threshold).astype(int)


def demo() -> None:
    rng = np.random.default_rng(7)
    x = rng.normal(size=(300, 2))
    y = (1.5 * x[:, 0] - x[:, 1] > 0.2).astype(int)
    model = LogisticRegressionGD(learning_rate=0.3, epochs=800).fit(x, y)
    accuracy = (model.predict(x) == y).mean()
    print("weights:", model.weights.round(3))
    print("bias:", round(model.bias, 3))
    print("accuracy:", round(float(accuracy), 3))


if __name__ == "__main__":
    demo()
