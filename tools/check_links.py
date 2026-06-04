#!/usr/bin/env python3
"""Validate local Markdown links.

The checker scans all Markdown files, ignores external links, ignores anchors when the target file
exists, reports broken local links, and exits non-zero when any broken link is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")


def iter_markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def is_external(target: str) -> bool:
    return target.startswith(EXTERNAL_PREFIXES)


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(strip_anchor(target))


def main() -> int:
    broken: list[str] = []
    for md_file in iter_markdown_files():
        text = md_file.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            if is_external(raw_target):
                continue
            target = normalize_target(raw_target)
            if not target:
                continue
            resolved = (md_file.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                broken.append(f"{md_file.relative_to(ROOT)} -> {raw_target} escapes repository")
                continue
            if not resolved.exists():
                broken.append(f"{md_file.relative_to(ROOT)} -> {raw_target}")

    if broken:
        print("Broken local Markdown links:")
        for item in broken:
            print(f"- {item}")
        return 1

    print(f"Checked {len(iter_markdown_files())} Markdown files. No broken local links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
