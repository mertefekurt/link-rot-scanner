"""Public package interface for link-rot-scanner."""

from link_rot_scanner.models import CheckResult, Link
from link_rot_scanner.scanner import scan_paths

__all__ = ["CheckResult", "Link", "scan_paths"]
