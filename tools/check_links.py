#!/usr/bin/env python3
"""Validate local Markdown links and local heading anchors."""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)

def iter_markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "__pycache__" not in path.parts
    )

def is_external(target: str) -> bool:
    return urlparse(target).scheme in EXTERNAL_SCHEMES

def split_target(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    path_part, _, anchor = target.partition("#")
    return unquote(path_part), unquote(anchor)

def github_anchor_slug(heading: str) -> str:
    heading = re.sub(r"`([^`]*)`", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    heading = re.sub(r"\s+", "-", heading)
    return heading

@lru_cache(maxsize=None)
def anchors_for(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for match in HEADING_RE.finditer(text):
        base = github_anchor_slug(match.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors

def main() -> int:
    broken: list[str] = []
    for md_file in iter_markdown_files():
        text = md_file.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw_target = match.group(1).strip()
            if is_external(raw_target):
                continue
            target_path, anchor = split_target(raw_target)
            resolved = (md_file.parent / target_path).resolve() if target_path else md_file.resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                broken.append(f"{md_file.relative_to(ROOT)} -> {raw_target} escapes repository")
                continue
            if not resolved.exists():
                broken.append(f"{md_file.relative_to(ROOT)} -> {raw_target}")
                continue
            if anchor and resolved.suffix == ".md" and anchor not in anchors_for(resolved):
                broken.append(f"{md_file.relative_to(ROOT)} -> {raw_target} missing heading anchor")

    if broken:
        print("Broken local Markdown links:")
        for item in broken:
            print(f"- {item}")
        return 1

    print(f"Checked {len(iter_markdown_files())} Markdown files. No broken local links found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
