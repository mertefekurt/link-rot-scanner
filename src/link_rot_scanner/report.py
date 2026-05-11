from __future__ import annotations

import json
from pathlib import Path

from link_rot_scanner.models import CheckResult


def render_table(results: list[CheckResult], root: Path) -> str:
    if not results:
        return "No Markdown links found."

    rows = [
        ("status", "source", "line", "target", "reason"),
        *[
            (
                result.status.upper(),
                _relative(result.link.source, root),
                str(result.link.line),
                result.link.target,
                result.reason,
            )
            for result in results
        ],
    ]
    widths = [max(len(row[index]) for row in rows) for index in range(len(rows[0]))]
    lines = [_format_row(rows[0], widths), _format_row(tuple("-" * width for width in widths), widths)]
    lines.extend(_format_row(row, widths) for row in rows[1:])
    lines.append("")
    lines.append(render_summary(results))
    return "\n".join(lines)


def render_json(results: list[CheckResult], root: Path) -> str:
    payload = [
        {
            "status": result.status,
            "source": _relative(result.link.source, root),
            "line": result.link.line,
            "target": result.link.target,
            "reason": result.reason,
            "resolved": result.resolved,
        }
        for result in results
    ]
    return json.dumps(payload, indent=2, sort_keys=True)


def render_summary(results: list[CheckResult]) -> str:
    ok = sum(1 for result in results if result.status == "ok")
    broken = sum(1 for result in results if result.status == "broken")
    skipped = sum(1 for result in results if result.status == "skipped")
    return f"Summary: {ok} ok, {broken} broken, {skipped} skipped"


def _format_row(row: tuple[str, ...], widths: list[int]) -> str:
    return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
