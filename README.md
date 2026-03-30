# litmap

<p align="center">
  <img src="docs/assets/litmap-logo.svg" alt="litmap logo" width="420">
</p>

<p align="center">
  <strong>Reproducible literature mapping in Python</strong>
</p>

<p align="center">
  Build a corpus, cluster in analysis space, project into display space, and export review-ready artifacts.
</p>

<p align="center">
  <a href="https://dai540.github.io/litmap/">Documentation</a> |
  <a href="https://dai540.github.io/litmap/tutorials/index.html">Tutorials</a> |
  <a href="docs/api.md">API</a> |
  <a href="https://github.com/dai540/litmap">Repository</a>
</p>

## Overview

`litmap` is a Python package for literature landscapes that stay inspectable after the run is over.
Instead of stopping at a figure, it organizes one run around explicit files:

- a canonical paper table
- embeddings and normalized representations
- cluster assignments and summaries
- 2D coordinates for display
- an interactive HTML map

The package is built around one design rule:

**cluster in analysis space, then plot in a separate display space.**

## Installation

```bash
pip install -e .
```

With optional extras:

```bash
pip install -e .[yaml]
pip install -e .[docs]
```

## Quick start

```bash
litmap init-config --output configs/my-run.yaml
litmap show-plan --config configs/default.yaml
litmap describe-layout
```

```python
from litmap import load_config, describe_pipeline, run_pipeline

config = load_config("configs/default.yaml")
steps = describe_pipeline(config)
result = run_pipeline(config)
```

## Run layout

```text
runs/
  my-topic/
    manifest.json
    config.snapshot.yaml
    raw/
    corpus/
    embeddings/
    analysis/
    reports/
```

Common outputs:

- `labels.csv`
- `cluster_summary.csv`
- `coords_2d.csv`
- `map_interactive.html`

## Documentation

The documentation site is the main entry point.

- [Docs home](https://dai540.github.io/litmap/)
- [Tutorial hub](https://dai540.github.io/litmap/tutorials/index.html)
- [Getting started](docs/getting-started.md)
- [Design notes](docs/design.md)
- [API surface](docs/api.md)

## Development

```bash
pytest
python -m build
mkdocs serve
```
