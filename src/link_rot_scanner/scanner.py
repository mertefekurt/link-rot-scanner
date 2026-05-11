from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

from link_rot_scanner.checker import LinkChecker
from link_rot_scanner.models import CheckResult
from link_rot_scanner.parser import parse_markdown_links

MARKDOWN_EXTENSIONS = {".md", ".markdown"}


def scan_paths(
    paths: Iterable[Path],
    *,
    timeout: float = 5.0,
    workers: int = 8,
    check_external: bool = True,
) -> list[CheckResult]:
    markdown_files = discover_markdown_files(paths)
    checker = LinkChecker(timeout=timeout, check_external=check_external)
    links = [link for path in markdown_files for link in parse_markdown_links(path)]

    if not links:
        return []

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        return list(executor.map(checker.check, links))


def discover_markdown_files(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved.is_file() and resolved.suffix.lower() in MARKDOWN_EXTENSIONS:
            files.append(resolved)
        elif resolved.is_dir():
            files.extend(
                candidate
                for candidate in sorted(resolved.rglob("*"))
                if candidate.is_file() and candidate.suffix.lower() in MARKDOWN_EXTENSIONS
            )
    return sorted(set(files))
