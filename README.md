# Link Rot Scanner

<p align="center">
  <img src="assets/readme-cover.svg" alt="Link Rot Scanner cover" width="100%" />
</p>

A fast CLI for finding broken Markdown links, local file references, and missing anchors.

## Working notes

- quick local checks around link health
- small CI jobs where a readable report is enough
- review workflows that need deterministic output

## Install

```bash
git clone https://github.com/mertefekurt/link-rot-scanner.git
cd link-rot-scanner
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Use

```bash
link-rot-scanner --help
```

## Files

```text
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
