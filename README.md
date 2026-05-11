![Project Banner](https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=180&section=header&text=link-rot-scanner&fontSize=50&fontAlignY=38)

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

# link-rot-scanner

Fast Markdown link auditing for docs-heavy repos.

| Checks | Handles |
| --- | --- |
| Local files | `docs/setup.md`, `../README.md` |
| Markdown anchors | `guide.md#install-steps` |
| External URLs | `https://example.com` |
| Reference links | `[docs]: https://example.com` |

![Code Snippet](assets/code-snapshot.png)

## Terminal

![Terminal Output](https://readme-typing-svg.demolab.com/?font=Fira+Code&weight=400&size=14&duration=1500&pause=500&center=false&vCenter=false&multiline=true&width=600&height=200&lines=link-rot-scanner+--no-external+.;Summary:+24+ok,+0+broken,+3+skipped)

## Install

```bash
python3 -m pip install -e .
```

## Usage

```bash
link-rot-scanner README.md docs/
link-rot-scanner --no-external .
link-rot-scanner --json --timeout 2 --workers 16 .
```

## CLI Reference

| Argument | Default | Purpose |
| --- | ---: | --- |
| `paths` | `.` | Markdown files or folders to scan |
| `--timeout` | `5.0` | HTTP timeout in seconds |
| `--workers` | `8` | Concurrent link checks |
| `--no-external` | `false` | Skip `http` and `https` URLs |
| `--json` | `false` | Print machine-readable results |

## Workflow

```mermaid
flowchart TD
    A["CLI input"] --> B["Discover Markdown files"]
    B --> C["Parse inline, reference, and autolinks"]
    C --> D{"Link type"}
    D --> E["Check local file path"]
    D --> F["Validate Markdown anchor"]
    D --> G["Probe external URL"]
    E --> H["Collect result"]
    F --> H
    G --> H
    H --> I["Render table or JSON"]
    I --> J{"Broken links?"}
    J -->|yes| K["Exit 1"]
    J -->|no| L["Exit 0"]
```

## Output Contract

| Status | Meaning | Exit impact |
| --- | --- | --- |
| `OK` | Target exists or URL responds | Success |
| `BROKEN` | Missing file, missing anchor, or failed URL | Exit code `1` |
| `SKIPPED` | Unsupported scheme or disabled external checks | Success |

## Project Layout

```text
src/link_rot_scanner/
  cli.py       # command-line interface
  parser.py    # Markdown link extraction
  checker.py   # local and external validation
  scanner.py   # discovery and concurrency
  report.py    # table and JSON rendering
tests/
  test_parser.py
  test_scanner.py
```
