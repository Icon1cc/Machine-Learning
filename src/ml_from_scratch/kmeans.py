"""Educational K-means clustering implemented with NumPy."""

from __future__ import annotations

import numpy as np


class KMeans:
    """Cluster points by alternating assignment and centroid updates."""

    def __init__(self, n_clusters: int = 3, max_iter: int = 100, random_state: int = 0) -> None:
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> "KMeans":
        x = np.asarray(x, dtype=float)
        rng = np.random.default_rng(self.random_state)
        indices = rng.choice(len(x), size=self.n_clusters, replace=False)
        centroids = x[indices].copy()

        for _ in range(self.max_iter):
            distances = ((x[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
            labels = distances.argmin(axis=1)
            new_centroids = np.vstack(
                [x[labels == cluster].mean(axis=0) if np.any(labels == cluster) else centroids[cluster]
                 for cluster in range(self.n_clusters)]
            )
            if np.allclose(new_centroids, centroids):
                break
            centroids = new_centroids

        self.centroids = centroids
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.centroids is None:
            raise RuntimeError("Model must be fitted before prediction.")
        x = np.asarray(x, dtype=float)
        distances = ((x[:, None, :] - self.centroids[None, :, :]) ** 2).sum(axis=2)
        return distances.argmin(axis=1)


def demo() -> None:
    rng = np.random.default_rng(3)
    x = np.vstack([
        rng.normal(loc=(-2, -2), scale=0.4, size=(50, 2)),
        rng.normal(loc=(2, 0), scale=0.4, size=(50, 2)),
        rng.normal(loc=(0, 2), scale=0.4, size=(50, 2)),
    ])
    model = KMeans(n_clusters=3, random_state=0).fit(x)
    print("centroids:")
    print(model.centroids.round(2))
    print("first ten labels:", model.predict(x[:10]))


if __name__ == "__main__":
    demo()
