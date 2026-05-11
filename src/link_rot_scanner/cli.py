from __future__ import annotations

import argparse
from pathlib import Path

from link_rot_scanner.report import render_json, render_table
from link_rot_scanner.scanner import scan_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="link-rot-scanner",
        description="Find broken Markdown links, local file references, and missing anchors.",
    )
    parser.add_argument("paths", nargs="*", type=Path, default=[Path(".")], help="Markdown files or folders to scan.")
    parser.add_argument("--timeout", type=float, default=5.0, help="External link timeout in seconds.")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent link checks.")
    parser.add_argument("--no-external", action="store_true", help="Skip http and https checks.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path.cwd().resolve()

    results = scan_paths(
        args.paths,
        timeout=args.timeout,
        workers=args.workers,
        check_external=not args.no_external,
    )

    print(render_json(results, root) if args.json else render_table(results, root))
    return 1 if any(result.is_problem for result in results) else 0
