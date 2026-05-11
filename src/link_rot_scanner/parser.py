from __future__ import annotations

import re
from pathlib import Path

from link_rot_scanner.models import Link

INLINE_LINK_PATTERN = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_LINK_PATTERN = re.compile(r"^[^\S\r\n]*\[([^\]]+)\]:[^\S\r\n]*(\S+)", re.MULTILINE)
AUTOLINK_PATTERN = re.compile(r"<(https?://[^>\s]+)>")


def parse_markdown_links(path: Path) -> list[Link]:
    text = path.read_text(encoding="utf-8")
    links: list[Link] = []

    for match in INLINE_LINK_PATTERN.finditer(text):
        label, target = match.groups()
        links.append(Link(path, _line_number(text, match.start()), label.strip(), target.strip()))

    for match in REFERENCE_LINK_PATTERN.finditer(text):
        label, target = match.groups()
        links.append(Link(path, _line_number(text, match.start()), label.strip(), target.strip()))

    for match in AUTOLINK_PATTERN.finditer(text):
        target = match.group(1)
        links.append(Link(path, _line_number(text, match.start()), target, target))

    return links


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1
