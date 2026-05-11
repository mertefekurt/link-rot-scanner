from __future__ import annotations

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from link_rot_scanner.anchors import collect_markdown_anchors
from link_rot_scanner.models import CheckResult, Link

SUPPORTED_EXTERNAL_SCHEMES = {"http", "https"}
SKIPPED_SCHEMES = {"mailto", "tel", "ftp"}


class LinkChecker:
    def __init__(self, *, timeout: float = 5.0, check_external: bool = True) -> None:
        self.timeout = timeout
        self.check_external = check_external
        self._anchor_cache: dict[Path, set[str]] = {}

    def check(self, link: Link) -> CheckResult:
        parsed = urlsplit(link.target)
        if parsed.scheme in SUPPORTED_EXTERNAL_SCHEMES:
            return self._check_external(link)
        if parsed.scheme in SKIPPED_SCHEMES:
            return CheckResult(link, "skipped", f"scheme '{parsed.scheme}' is not checked", link.target)
        if parsed.scheme:
            return CheckResult(link, "skipped", f"unsupported scheme '{parsed.scheme}'", link.target)
        return self._check_local(link)

    def _check_external(self, link: Link) -> CheckResult:
        if not self.check_external:
            return CheckResult(link, "skipped", "external checks disabled", link.target)

        request = Request(link.target, method="HEAD", headers={"User-Agent": "link-rot-scanner/0.1"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return CheckResult(link, "ok", f"http {response.status}", link.target)
        except HTTPError as error:
            if error.code in {405, 429}:
                return self._check_external_with_get(link)
            return CheckResult(link, "broken", f"http {error.code}", link.target)
        except URLError as error:
            return CheckResult(link, "broken", str(error.reason), link.target)
        except TimeoutError:
            return CheckResult(link, "broken", "request timed out", link.target)

    def _check_external_with_get(self, link: Link) -> CheckResult:
        request = Request(link.target, method="GET", headers={"User-Agent": "link-rot-scanner/0.1"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return CheckResult(link, "ok", f"http {response.status}", link.target)
        except HTTPError as error:
            return CheckResult(link, "broken", f"http {error.code}", link.target)
        except URLError as error:
            return CheckResult(link, "broken", str(error.reason), link.target)
        except TimeoutError:
            return CheckResult(link, "broken", "request timed out", link.target)

    def _check_local(self, link: Link) -> CheckResult:
        parsed = urlsplit(link.target)
        raw_path = unquote(parsed.path)
        target_path = link.source if raw_path == "" else (link.source.parent / raw_path).resolve()

        if not target_path.exists():
            return CheckResult(link, "broken", "target file does not exist", str(target_path))
        if parsed.fragment:
            return self._check_anchor(link, target_path, unquote(parsed.fragment))
        return CheckResult(link, "ok", "local target exists", str(target_path))

    def _check_anchor(self, link: Link, target_path: Path, fragment: str) -> CheckResult:
        if target_path.suffix.lower() not in {".md", ".markdown"}:
            return CheckResult(link, "skipped", "anchor target is not Markdown", str(target_path))

        anchors = self._anchor_cache.setdefault(target_path, collect_markdown_anchors(target_path))
        normalized_fragment = fragment.lower()
        if normalized_fragment in anchors:
            return CheckResult(link, "ok", "anchor exists", f"{target_path}#{fragment}")
        return CheckResult(link, "broken", f"anchor '{fragment}' does not exist", f"{target_path}#{fragment}")
