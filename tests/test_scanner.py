from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from link_rot_scanner.scanner import scan_paths


class ScannerTests(unittest.TestCase):
    def test_reports_missing_local_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("[Missing](docs/missing.md)\n", encoding="utf-8")

            results = scan_paths([readme], check_external=False)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "broken")
        self.assertEqual(results[0].reason, "target file does not exist")

    def test_validates_markdown_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guide = root / "guide.md"
            guide.write_text("# Install Steps\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("[Install](guide.md#install-steps)\n[Bad](guide.md#missing)\n", encoding="utf-8")

            results = scan_paths([readme], check_external=False)

        self.assertEqual([result.status for result in results], ["ok", "broken"])
        self.assertEqual(results[1].reason, "anchor 'missing' does not exist")


if __name__ == "__main__":
    unittest.main()
