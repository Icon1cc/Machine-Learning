#!/usr/bin/env python3
"""
Rewrite templated learning files with topic-specific content.

Reads CONTENT dicts from one or more data modules in tools/, locates the
matching markdown file, and writes a fully formed lesson. Preserves the
existing Navigation footer (so links stay valid).

Run: python3 tools/rewrite_topics.py
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def load_content_dict(module_path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {module_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "CONTENT", {})


def render_lesson(rel_path: str, data: dict, nav_footer: str) -> str:
    """Build a full markdown lesson from a content dict + the existing nav footer."""
    title = data["title"]
    intuition = data["intuition"].strip()
    formal = data["formal"].strip()
    why = data["why"].strip()
    steps = data["steps"]
    example = data["example"].strip()
    mistakes = data["mistakes"]
    iq = data["iq"].strip()
    is_strong = data["is_strong"].strip()
    is_weak = data["is_weak"].strip()
    follow_ups = data["follow_ups"]
    exercise = data["exercise"].strip()
    diagram = data["diagram"].strip()

    steps_md = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
    mistakes_md = "\n".join(f"- {m}" for m in mistakes)
    follow_ups_md = "\n".join(f"- {q}" for q in follow_ups)

    body = f"""# {title}

## Beginner-Friendly Intuition

{intuition}

## Formal Explanation

{formal}

## Why It Matters in Real Jobs

{why}

## How It Works Step by Step

{steps_md}

## Real-World Example

{example}

## Common Mistakes

{mistakes_md}

## Interview Angle

**Question:** {iq}

**Strong answer:** {is_strong}

**Weak answer:** {is_weak}

**Follow-up questions:**

{follow_ups_md}

## Mini Exercise

{exercise}

## Diagram

```mermaid
{diagram}
```

---
{nav_footer}
"""
    return body


NAV_RE = re.compile(r"^## Navigation\n\n\[⬅ Previous\].*?\| \[🏠 Home\].*?\| \[➡ Next\].*?$", re.MULTILINE)


def extract_nav(text: str) -> str | None:
    """Return the existing '## Navigation\\n\\n[⬅ Previous]...' block (without the leading '---')."""
    match = NAV_RE.search(text)
    if not match:
        return None
    return match.group(0)


def rewrite_one(rel_path: str, data: dict) -> str:
    file_path = ROOT / rel_path
    if not file_path.exists():
        return f"missing: {rel_path}"
    original = file_path.read_text(encoding="utf-8")
    nav = extract_nav(original)
    if nav is None:
        return f"no-nav: {rel_path}"
    new_text = render_lesson(rel_path, data, nav)
    file_path.write_text(new_text, encoding="utf-8")
    return f"ok: {rel_path}"


def main() -> int:
    data_modules = sorted(TOOLS.glob("content_data*.py"))
    merged: dict = {}
    for mod_path in data_modules:
        d = load_content_dict(mod_path)
        merged.update(d)
    if not merged:
        print("No content data found", file=sys.stderr)
        return 1

    results = []
    for rel_path, data in merged.items():
        results.append(rewrite_one(rel_path, data))
    ok = sum(1 for r in results if r.startswith("ok:"))
    print(f"Rewrote {ok}/{len(results)} files.")
    for r in results:
        if not r.startswith("ok:"):
            print("  ", r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
