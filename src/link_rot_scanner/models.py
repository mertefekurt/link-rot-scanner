from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

LinkStatus = Literal["ok", "broken", "skipped"]


@dataclass(frozen=True)
class Link:
    source: Path
    line: int
    label: str
    target: str


@dataclass(frozen=True)
class CheckResult:
    link: Link
    status: LinkStatus
    reason: str
    resolved: str

    @property
    def is_problem(self) -> bool:
        return self.status == "broken"
