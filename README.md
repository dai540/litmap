# litmap

<p align="center">
  <img src="docs/assets/litmap-icon.svg" alt="litmap icon" width="64">
</p>

<p align="center"><strong>Reproducible literature mapping in Python.</strong></p>

<p align="center">
  <a href="https://dai540.github.io/litmap/">Documentation</a> |
  <a href="https://dai540.github.io/litmap/tutorials/index.html">Tutorials</a> |
  <a href="https://github.com/dai540/litmap">GitHub</a>
</p>

`litmap` is a Python package for building literature landscapes that stay readable after the run is over. The package is organized around explicit artifacts: a canonical paper table, embeddings, clustering outputs, 2D coordinates, and an interactive map.

Like the documentation site, this README is meant to answer three questions quickly:

1. What does the package do?
2. Where should I start reading?
3. What files come out of one run?

## What litmap does

`litmap` treats one analysis as a simple architecture:

1. define a corpus
2. normalize paper records
3. build embeddings
4. cluster in analysis space
5. project into a separate 2D display space
6. export review-ready artifacts

The core design rule is: **cluster in analysis space, plot in display space**.

## Start here

| Page | Why it exists |
| --- | --- |
| [Documentation home](https://dai540.github.io/litmap/) | Main entry point with the site map and pipeline overview |
| [Tutorials](https://dai540.github.io/litmap/tutorials/index.html) | Worked case studies with maps, tables, and interpretation |
| [Getting started](docs/getting-started.md) | Installation, commands, and run layout |
| [Design notes](docs/design.md) | Architecture, run semantics, and artifact boundaries |
| [API surface](docs/api.md) | Stable Python entry points |

## Installation

Editable install:

```bash
pip install -e .
```

With YAML support:

```bash
pip install -e .[yaml]
```

With docs tooling:

```bash
pip install -e .[docs]
mkdocs serve
```

## Package shape

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

Expected outputs include:

- `labels.csv`
- `cluster_summary.csv`
- `coords_2d.csv`
- `map_interactive.html`

## Public entry points

CLI:

```bash
litmap version
litmap init-config --output configs/my-run.yaml
litmap describe-layout
litmap show-plan --config configs/default.yaml
```

Python:

```python
from litmap import load_config, describe_pipeline, run_pipeline

config = load_config("configs/default.yaml")
steps = describe_pipeline(config)
result = run_pipeline(config)
```

## Documentation style

The project docs are intentionally closer to a package documentation site than to a notebook dump. The home page is a map of the project, and the tutorial pages are long-form case studies that end in concrete artifacts a review team could inspect.

## Development

```bash
pytest
python -m build
```
