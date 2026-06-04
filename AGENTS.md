# AGENTS.md

## Repository Purpose

This repository is a self-contained Machine Learning Bible for AI Engineer, Machine Learning
Engineer, LLM Engineer, Data Scientist, Applied Scientist, and GenAI Engineer preparation.

## Important Directories

- `fundamentals/` through `ethics-safety/`: ordered learning lessons.
- `case-studies/`: production-style ML and AI case studies.
- `interview-prep/`, `mocks/`, `quizzes/`, `cheatsheets/`: interview preparation.
- `capstone-projects/`: portfolio project guides.
- `notebooks/`: starter notebooks for hands-on learning.
- `src/`: runnable educational Python examples.
- `tools/`: repository maintenance scripts.

## Commands

- Install: `pip install -r requirements.txt`
- Generate index: `python tools/generate_repo_index.py`
- Check links: `python tools/check_links.py`
- Run examples: `python src/ml_from_scratch/linear_regression.py`
- Run tests: no dedicated test suite is currently defined; verify tools and examples directly.

## Files Agents Should Not Edit Casually

- Generated caches such as `__pycache__/`, `.pytest_cache/`, `.ipynb_checkpoints/`.
- Virtual environments and local data folders.
- `REPO_INDEX.md` should be regenerated with `python tools/generate_repo_index.py`.

## Coding and Writing Conventions

- Keep numeric prefixes for reading order.
- Every Markdown learning file must teach with intuition, formal explanation, job relevance,
  step-by-step mechanics, examples, mistakes, interview angle, exercise, diagram where useful, and
  final navigation.
- Do not add fake citations or external references that are not actually used.
- Python examples must run locally without API keys.
- Prefer clear, educational code over clever abstractions.

## Standing Rules

- Before editing, map the relevant files, tests, entry points, and data flow.
- For framework or library behavior, check local package versions first, then use Context7 before
  guessing.
- For OpenAI API work, use OpenAI Developer Docs.
- For browser/UI bugs, use Playwright and Chrome DevTools.
- For non-trivial changes, prefer the smallest safe change and avoid unrelated refactors.
- For behavior changes, add or update tests when practical.
- Run the narrowest relevant verification first.
- Report exact commands run and what passed or failed.

## Definition of Done

A change is done when content is complete, links pass, relevant examples run, no empty files are
introduced, and the final response reports verification honestly.

---
## Navigation

[⬅ Previous](CHANGELOG.md) | [🏠 Home](README.md) | [➡ Next](fundamentals/01-what-is-machine-learning.md)
