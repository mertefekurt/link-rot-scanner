# Link Rot Scanner

A fast CLI for finding broken Markdown links, local file references, and missing anchors. The idea is simple: give Link Rot Scanner the local file or fixture, get a readable result, and decide what needs attention before the next handoff.

## A quick look

![Link Rot Scanner cover](assets/readme-cover.svg)

## Start here

```bash
git clone https://github.com/mertefekurt/link-rot-scanner.git
cd link-rot-scanner
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run:

```bash
link-rot-scanner --help
```

## Files with the most context

```text
src/            package source
tests/          test coverage
.gitignore      project file
pyproject.toml  package metadata
```
