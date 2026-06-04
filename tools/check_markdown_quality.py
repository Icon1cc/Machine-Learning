#!/usr/bin/env python3
"""Validate Markdown structure, naming, navigation, and formatting."""

from __future__ import annotations

import re
import sys
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

NAV_RE = re.compile(
    r"---\n## Navigation\n\n"
    r"\[⬅ Previous\]\([^)]+\) \| "
    r"\[🏠 Home\]\([^)]+\) \| "
    r"\[➡ Next\]\([^)]+\)\s*$"
)

def phrase(*parts: str) -> str:
    return "".join(parts)

FORBIDDEN_ROOT_FILES = [
    phrase("CODE", "_OF_CONDUCT.md"),
    phrase("CONTRIB", "UTING.md"),
    phrase("CHANGE", "LOG.md"),
    phrase("F", "AQ.md"),
    phrase("AG", "ENTS.md"),
]

BANNED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\b" + phrase("Bi", "ble") + r"\b",
        r"\b" + phrase("Complete", " Guide") + r"\b",
        r"\b" + phrase("Ulti", "mate") + r"\b",
        r"\b" + phrase("Master", " Guide") + r"\b",
        phrase("Holy", " Grail"),
        phrase("Complete", " mastery"),
        phrase("Guaranteed", " success"),
        phrase("Learn", " everything"),
    ]
]

REQUIRED_ROOT_SECTIONS = [
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

TOPIC_REQUIRED = [
    "intuition",
    "formal explanation",
    "why it matters",
    "how it works",
    "real-world example",
    "common mistakes",
    "interview angle",
    "mini exercise",
]

CASE_STUDY_REQUIRED = [
    "problem statement",
    "functional requirements",
    "non-functional requirements",
    "assumptions",
    "architecture diagram",
    "data model or data design",
    "api design",
    "scaling strategy",
    "reliability strategy",
    "security considerations",
    "observability",
    "bottlenecks",
    "tradeoffs",
    "interview explanation script",
    "follow-up questions",
    "common mistakes",
]

MOCK_REQUIRED = [
    "round format",
    "interviewer prompt",
    "expected clarification questions",
    "expected answer or design",
    "scoring rubric",
    "red flags",
    "self-review checklist",
]

def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )

def numbered_markdown(folder: str) -> list[Path]:
    return sorted(
        path
        for path in (ROOT / folder).glob("*.md")
        if path.name != "README.md"
    )

def title_heading(text: str) -> bool:
    return bool(re.search(r"^#\s+\S+", text, flags=re.MULTILINE))

def has_closed_fences(text: str) -> bool:
    return text.count("```") % 2 == 0

def section_present(text: str, section: str) -> bool:
    return section.lower() in text.lower()

def report(errors: list[str], message: str) -> None:
    errors.append(message)

def check_root_readme(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        report(errors, "README.md is missing.")
        return
    text = readme.read_text(encoding="utf-8")
    if not text.startswith("# Machine Learning\n"):
        report(errors, "README.md must start with '# Machine Learning'.")
    if "```mermaid" not in text:
        report(errors, "README.md must include a Mermaid roadmap.")
    if NAV_RE.search(text):
        report(errors, "README.md should not end with previous/next navigation.")
    for section in REQUIRED_ROOT_SECTIONS:
        if f"## {section}" not in text:
            report(errors, f"README.md missing required section: {section}.")

def check_forbidden_root_files(errors: list[str]) -> None:
    for name in FORBIDDEN_ROOT_FILES:
        if (ROOT / name).exists():
            report(errors, f"{name} should not exist in this personal learning repository.")

def check_major_folder_readmes(errors: list[str]) -> None:
    for folder in MAJOR_FOLDERS:
        readme = ROOT / folder / "README.md"
        if not readme.exists():
            report(errors, f"{folder}/README.md is missing.")
            continue
        text = readme.read_text(encoding="utf-8")
        for required in [
            "Folder Purpose",
            "Who Should Read This Section",
            "Recommended Reading Order",
            "Table of Contents",
            "What You Should Know After Finishing",
            "Suggested Exercises",
            "Navigation",
        ]:
            if f"## {required}" not in text:
                report(errors, f"{folder}/README.md missing section: {required}.")
        if "../README.md" not in text and folder != ".":
            report(errors, f"{folder}/README.md must link back to root README.md.")

def check_numbering(errors: list[str]) -> None:
    valid_name = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*\.md$")
    for folder in LEARNING_FOLDERS:
        paths = numbered_markdown(folder)
        numbers: list[int] = []
        for path in paths:
            if not valid_name.match(path.name):
                report(errors, f"{path.relative_to(ROOT)} must use a two-digit lowercase numeric prefix.")
                continue
            number = int(path.name[:2])
            numbers.append(number)
        if numbers:
            expected = list(range(1, len(numbers) + 1))
            if sorted(numbers) != expected:
                report(
                    errors,
                    f"{folder}/ numbering must be contiguous from 01 to {len(numbers):02d}. Found {sorted(numbers)}.",
                )

def check_notebook_numbering(errors: list[str]) -> None:
    valid_name = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*\.ipynb$")
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    numbers: list[int] = []
    for path in notebooks:
        if not valid_name.match(path.name):
            report(errors, f"{path.relative_to(ROOT)} must use a two-digit tutorial notebook prefix.")
            continue
        numbers.append(int(path.name[:2]))
    if numbers and sorted(numbers) != list(range(1, len(numbers) + 1)):
        report(errors, f"notebooks/ numbering must be contiguous from 01 to {len(numbers):02d}.")

def check_learning_navigation(errors: list[str]) -> None:
    for folder in LEARNING_FOLDERS:
        for path in numbered_markdown(folder):
            text = path.read_text(encoding="utf-8")
            if not NAV_RE.search(text):
                report(errors, f"{path.relative_to(ROOT)} missing valid final Navigation block.")
            if "[🏠 Home](" in text and "/Users/" in text:
                report(errors, f"{path.relative_to(ROOT)} contains an absolute local path in navigation.")

def check_content_sections(errors: list[str]) -> None:
    topic_folders = [
        folder
        for folder in LEARNING_FOLDERS
        if folder not in {"case-studies", "interview-prep", "mocks", "quizzes", "cheatsheets", "capstone-projects"}
    ]
    for folder in topic_folders:
        for path in numbered_markdown(folder):
            text = path.read_text(encoding="utf-8")
            for section in TOPIC_REQUIRED:
                if not section_present(text, section):
                    report(errors, f"{path.relative_to(ROOT)} missing topic section: {section}.")
            if "```mermaid" not in text:
                report(errors, f"{path.relative_to(ROOT)} should include a Mermaid diagram.")
    for path in numbered_markdown("case-studies"):
        text = path.read_text(encoding="utf-8")
        for section in CASE_STUDY_REQUIRED:
            if not section_present(text, section):
                report(errors, f"{path.relative_to(ROOT)} missing case study section: {section}.")
    for path in numbered_markdown("mocks"):
        text = path.read_text(encoding="utf-8")
        for section in MOCK_REQUIRED:
            if not section_present(text, section):
                report(errors, f"{path.relative_to(ROOT)} missing mock section: {section}.")
    for path in numbered_markdown("quizzes"):
        text = path.read_text(encoding="utf-8")
        if len(re.findall(r"^\d+\.", text, flags=re.MULTILINE)) < 20:
            report(errors, f"{path.relative_to(ROOT)} should include 10 questions and 10 answer explanations.")
        if "## Answer Key" not in text:
            report(errors, f"{path.relative_to(ROOT)} missing answer key.")

def check_markdown_basics(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if not text.strip():
            report(errors, f"{rel} is empty.")
        if not title_heading(text):
            report(errors, f"{rel} missing title heading.")
        if "\u2014" in text:
            report(errors, f"{rel} contains an em dash character.")
        for pattern in BANNED_PATTERNS:
            if pattern.search(text):
                report(errors, f"{rel} contains banned phrase matching {pattern.pattern!r}.")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "TODO" in line and "exercise" not in line.lower():
                report(errors, f"{rel}:{line_number} contains a TODO placeholder outside an exercise.")
        if not has_closed_fences(text):
            report(errors, f"{rel} has unclosed Markdown code fences.")
        minimum = 300 if path.name == "README.md" else 500
        if path.parent == ROOT and path.name not in {"README.md", "REPO_INDEX.md"}:
            minimum = 120
        if len(text.strip()) < minimum:
            report(errors, f"{rel} is too short to be useful.")

def main() -> int:
    errors: list[str] = []
    check_root_readme(errors)
    check_forbidden_root_files(errors)
    check_major_folder_readmes(errors)
    check_numbering(errors)
    check_notebook_numbering(errors)
    check_learning_navigation(errors)
    check_content_sections(errors)
    check_markdown_basics(errors)

    if errors:
        print("Markdown quality check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Markdown quality check passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
