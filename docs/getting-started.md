# Getting Started

## Installation

Minimal editable install:

```bash
pip install -e .
```

YAML config support:

```bash
pip install -e .[yaml]
```

Intended analysis stack:

```bash
pip install -e .[full]
```

Documentation stack:

```bash
pip install -e .[docs]
mkdocs serve
```

Rebuild the bundled tutorial outputs:

```bash
"C:\Program Files\LibreOffice\program\python.exe" scripts/build_case_studies.py
```

## Command line

```bash
litmap version
litmap init-config --output configs/my-run.yaml
litmap describe-layout
litmap show-plan --config configs/default.yaml
```

## Package layout

```text
src/litmap/
  config/
  domain/
  sources/
  corpus/
  embed/
  analyze/
  visualize/
  storage/
  pipeline/
  cli/
```

## What a polished package experience should provide

- a clear README with installation and scope
- a static documentation site that goes beyond the README
- multiple tutorials, not just one quickstart
- sample outputs that make the final deliverables tangible
- a repeatable script that regenerates tutorial artifacts from bundled corpora
- a stable API surface that future implementations can grow behind
