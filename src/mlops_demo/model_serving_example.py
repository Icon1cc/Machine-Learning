"""Minimal model serving example using only the Python standard library.

Run:
    python src/mlops_demo/model_serving_example.py

Then open:
    http://127.0.0.1:8000/predict?x=2.5
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def predict(x_value: float) -> float:
    """A tiny deterministic model: y = 2x + 1."""
    return 2.0 * x_value + 1.0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/predict":
            self.send_error(404, "Use /predict?x=<number>")
            return

        query = parse_qs(parsed.query)
        try:
            x_value = float(query.get("x", [""])[0])
        except ValueError:
            self.send_error(400, "Query parameter x must be a number.")
            return

        payload = json.dumps({"x": x_value, "prediction": predict(x_value)}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("Serving on http://127.0.0.1:8000/predict?x=2.5")
    server.serve_forever()


if __name__ == "__main__":
    main()
