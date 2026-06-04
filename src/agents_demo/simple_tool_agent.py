"""A deterministic, API-free example of a tool-using agent loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


Tool = Callable[[str], str]


def calculator(expression: str) -> str:
    """Evaluate a tiny safe arithmetic expression for demo purposes."""
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        return "calculator error: unsupported character"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"calculator error: {exc}"


def lookup_policy(query: str) -> str:
    policies = {
        "vacation": "Employees receive 20 vacation days per year.",
        "expenses": "Expenses must be filed within 30 days.",
    }
    return policies.get(query.lower(), "No matching policy found.")


@dataclass
class SimpleAgent:
    tools: dict[str, Tool]

    def run(self, goal: str) -> str:
        """Choose a tool with simple rules, observe the result, and return a final answer."""
        if "calculate" in goal.lower():
            expression = goal.lower().split("calculate", 1)[1].strip()
            observation = self.tools["calculator"](expression)
            return f"I calculated the result: {observation}"
        if "vacation" in goal.lower():
            observation = self.tools["policy"]("vacation")
            return f"I checked the policy: {observation}"
        return "I do not have a suitable tool for this goal."


def demo() -> None:
    agent = SimpleAgent({"calculator": calculator, "policy": lookup_policy})
    print(agent.run("Calculate 12 * (3 + 4)"))
    print(agent.run("What is the vacation policy?"))


if __name__ == "__main__":
    demo()
