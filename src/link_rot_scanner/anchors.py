from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
PUNCTUATION_PATTERN = re.compile(r"[^\w\s-]")
SPACE_PATTERN = re.compile(r"[\s-]+")


def collect_markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: defaultdict[str, int] = defaultdict(int)

    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        base = github_anchor(match.group(2))
        index = seen[base]
        seen[base] += 1
        anchors.add(base if index == 0 else f"{base}-{index}")

    return anchors


def github_anchor(heading: str) -> str:
    normalized = PUNCTUATION_PATTERN.sub("", heading.strip().lower())
    return SPACE_PATTERN.sub("-", normalized).strip("-")
