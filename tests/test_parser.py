from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from link_rot_scanner.parser import parse_markdown_links


class ParserTests(unittest.TestCase):
    def test_parses_inline_reference_and_autolinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(
                "[Guide](docs/guide.md)\n\n"
                "[site]: https://example.com\n"
                "<https://example.org>\n"
                "![Image](assets/logo.png)\n",
                encoding="utf-8",
            )

            links = parse_markdown_links(path)

        self.assertEqual([link.target for link in links], ["docs/guide.md", "https://example.com", "https://example.org"])
        self.assertEqual([link.line for link in links], [1, 3, 4])


if __name__ == "__main__":
    unittest.main()
