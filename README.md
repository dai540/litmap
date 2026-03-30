# litmap

<p align="center">
  <img src="docs/assets/litmap-icon.svg" alt="litmap icon" width="120">
</p>

`litmap` is a Python package for reproducible literature mapping.
It is meant for workflows where you need more than a notebook screenshot: you
need a map, a label table, a cluster summary, and a traceable run directory.

Project site:

- Repository: [github.com/dai540/litmap](https://github.com/dai540/litmap)
- Docs and tutorials: [dai540.github.io/litmap](https://dai540.github.io/litmap/)

The package treats literature mapping as a sequence of explicit stages:

1. source ingestion
2. corpus preparation
3. embedding
4. analysis-space reduction and clustering
5. display-space projection
6. interactive map export

That structure keeps clustering logic separate from visual layout and makes the
resulting outputs easier to trust, debug, and share.

## What this repository includes

- installable package with `src/` layout and console entry point
- typed configuration model with YAML or JSON loading
- run-oriented artifact layout with `manifest.json` and `config.snapshot.yaml`
- package modules split by responsibility rather than by notebook step
- a MkDocs-based documentation site, analogous to `pkgdown` in the R ecosystem
- multiple tutorials with bundled result artifacts and figures

## Installation

Minimal editable install:

```bash
pip install -e .
```

Editable install with YAML support:

```bash
pip install -e .[yaml]
```

Editable install with the intended analysis stack:

```bash
pip install -e .[full]
```

Editable install with documentation tooling:

```bash
pip install -e .[docs]
mkdocs serve
```

## Command line

```bash
litmap version
litmap init-config --output configs/my-run.yaml
litmap describe-layout
litmap show-plan --config configs/default.yaml
```

## Python API

```python
from litmap import load_config, describe_pipeline, run_pipeline

config = load_config("configs/default.yaml")
steps = describe_pipeline(config)
result = run_pipeline(config)
```

`describe_pipeline()` gives a stable blueprint of the intended stages and
outputs. `run_pipeline()` currently returns a structured run description and is
the public boundary that future execution backends should keep.

## Output layout

`litmap` treats the run directory as part of the package contract:

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

The recommended run name is human-readable, such as `my-topic` or
`immunotherapy-landscape`. It should not depend on a timestamp.

## Documentation site

The long-form documentation lives in `docs/` and is designed to be built into a
static HTML site with MkDocs. This is the Python-side analogue of `pkgdown`.

Main entry points:

- Docs home: [docs/index.md](docs/index.md)
- Getting started: [docs/getting-started.md](docs/getting-started.md)
- Design notes: [docs/design.md](docs/design.md)
- API surface: [docs/api.md](docs/api.md)
- Tutorials index: [docs/tutorials/index.md](docs/tutorials/index.md)

## Tutorials and bundled outputs

The tutorials are written to end at concrete outputs a user would care about:

- `labels.csv`
- `cluster_summary.csv`
- `coords_2d.csv`
- `map_interactive.html`

Included tutorial articles:

- [Immunotherapy Landscape](docs/tutorials/immunotherapy-landscape.md)
- [OpenAlex Topic Scan](docs/tutorials/openalex-topic-scan.md)
- [Local CSV Corpus](docs/tutorials/local-csv-corpus.md)
- [Target Discovery Omics](docs/tutorials/target-discovery-omics.md)
- [ADMET and Safety Landscape](docs/tutorials/admet-safety-landscape.md)
- [Translational Biomarker Stratification](docs/tutorials/translational-biomarker-stratification.md)

Bundled case-study outputs:

- [docs/case-studies/immunotherapy-landscape](docs/case-studies/immunotherapy-landscape)
- [docs/case-studies/openalex-topic-scan](docs/case-studies/openalex-topic-scan)
- [docs/case-studies/local-csv-corpus](docs/case-studies/local-csv-corpus)

## Design principles

- Reproducibility before convenience
- Explicit artifacts before hidden state
- Source adapters at the boundary
- Analysis space and display space kept separate
- Thin CLI over a reusable Python API
- Documentation should show final outputs, not only setup commands

## Project status

This repository now has the structure and packaging expected from a serious
Python package and a Python-native static docs workflow. The computational
backends are still evolving behind that interface. The documentation case
studies are generated from bundled tutorial corpora by
`scripts/build_case_studies.py`, which provides an actual deterministic analysis
path for the docs without relying on heavyweight external dependencies.

## Development

```bash
pytest
python -m build
```
