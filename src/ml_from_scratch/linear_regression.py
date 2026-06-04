"""Educational linear regression with batch gradient descent."""

from __future__ import annotations

import numpy as np


class LinearRegressionGD:
    """Fit y = Xw + b by minimizing mean squared error."""

    def __init__(self, learning_rate: float = 0.05, epochs: int = 1000) -> None:
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights: np.ndarray | None = None
        self.bias = 0.0

    def fit(self, x: np.ndarray, y: np.ndarray) -> "LinearRegressionGD":
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        self.weights = np.zeros(x.shape[1])
        self.bias = 0.0

        for _ in range(self.epochs):
            predictions = x @ self.weights + self.bias
            errors = predictions - y
            self.weights -= self.learning_rate * (2 / len(x)) * (x.T @ errors)
            self.bias -= self.learning_rate * 2 * errors.mean()
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.weights is None:
            raise RuntimeError("Model must be fitted before prediction.")
        return np.asarray(x, dtype=float) @ self.weights + self.bias


def demo() -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(size=(200, 2))
    y = 3.0 * x[:, 0] - 2.0 * x[:, 1] + 0.5 + rng.normal(scale=0.1, size=200)
    model = LinearRegressionGD(learning_rate=0.05, epochs=800).fit(x, y)
    mse = np.mean((model.predict(x) - y) ** 2)
    print("weights:", model.weights.round(3))
    print("bias:", round(model.bias, 3))
    print("mse:", round(float(mse), 4))


if __name__ == "__main__":
    demo()
