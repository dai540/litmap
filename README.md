# litmap

<img src="docs/assets/litmap-icon.svg" alt="litmap icon" width="92" />

[![Docs](https://img.shields.io/badge/docs-github.io-0f6c63)](https://dai540.github.io/litmap/)
![Python](https://img.shields.io/badge/python-3.10%2B-3776ab)
![License](https://img.shields.io/badge/license-MIT-0f172a)
![Status](https://img.shields.io/badge/status-alpha-b65a2a)

`litmap` is a Python package for reproducible literature mapping. It is built around explicit run artifacts, a clean separation between analysis space and display space, and a Sphinx documentation site that is meant to be read as a real package site rather than a notebook dump.

- Read the docs: [https://dai540.github.io/litmap/](https://dai540.github.io/litmap/)
- Browse tutorials: [Tutorials](docs/tutorials/index.md)
- Start from the package overview: [Home](docs/index.md)
- Inspect the package surface: [API](docs/api.md)

## Install

Install from a local clone:

```bash
pip install -e .[yaml,docs]
```

Install the broader analysis stack when needed:

```bash
pip install -e .[full]
```

## Build the Sphinx docs

```bash
sphinx-build -b html docs docs/_build/html
```

## Get started

```bash
litmap init-config --output configs/my-run.yaml
litmap show-plan --config configs/default.yaml
litmap describe-layout
```

Then inspect:

- `configs/default.yaml`
- `docs/index.md`
- `docs/tutorials/index.md`
- `runs/<topic>/`

## What this package is for

`litmap` is designed for questions like these:

- what topical neighborhoods emerge in a literature corpus when cluster count is not fixed in advance
- which papers belong to dense thematic clusters versus ambiguous bridge regions
- how should clustering logic be separated from the 2D layout used for communication
- what artifacts should be saved so the run remains interpretable later

## Public API

The intended public package surface is small:

- `litmap.load_config`
- `litmap.describe_pipeline`
- `litmap.run_pipeline`
- `litmap.LitmapConfig`
- `litmap.cli`

The project does not promise stability for undocumented internal details.

## Current highlights

- Sphinx-based package documentation with GitHub Pages deployment
- tutorial-first case-study articles
- explicit run layout with `manifest.json` and `config.snapshot.yaml`
- architecture centered on analysis space versus display space
- generated result artifacts such as `labels.csv`, `cluster_summary.csv`, and `map_interactive.html`

## Current limitation

The package surface and documentation are ahead of the final computational backend. `litmap` should currently be understood as a strong package and documentation scaffold with deterministic tutorial pipelines while the final embedding and clustering backend continues to mature.

## Documentation map

- [Home](docs/index.md)
- [Tutorials](docs/tutorials/index.md)
- [Getting started](docs/getting-started.md)
- [Design](docs/design.md)
- [API](docs/api.md)
