# Getting started

## Install

Install from a local clone:

```bash
pip install -e .[yaml,docs]
```

Install the broader analysis stack when you want the intended scientific dependencies:

```bash
pip install -e .[full]
```

Build the Sphinx site locally:

```bash
sphinx-build -b html docs docs/_build/html
```

## First commands

```bash
litmap version
litmap init-config --output configs/my-run.yaml
litmap show-plan --config configs/default.yaml
litmap describe-layout
```

## Public Python entry points

```python
from litmap import LitmapConfig, describe_pipeline, load_config, run_pipeline

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

Common outputs include:

- `labels.csv`
- `cluster_summary.csv`
- `coords_2d.csv`
- `map_interactive.html`

## What to read next

- If you want examples first, go to [Tutorials](tutorials/index.md).
- If you want the package rationale, go to [Design](design.md).
- If you want the stable interface, go to [API](api.md).
