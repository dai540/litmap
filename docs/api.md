# API Surface

## Public imports

```python
from litmap import LitmapConfig, load_config, describe_pipeline, run_pipeline
```

## Current public API

### `load_config(path)`

Load YAML or JSON configuration into a typed `LitmapConfig`.

### `describe_pipeline(config)`

Return a stable description of the intended pipeline stages and outputs.

### `run_pipeline(config, run_dir=None)`

Return a structured run description. This is the boundary that future execution
backends should preserve.

## Public configuration object

`LitmapConfig` contains:

- `project`
- `source`
- `corpus`
- `embedding`
- `analysis`
- `visualization`
- `output`
- `runtime`

## Extension boundaries

The most natural extension points are:

- new source adapters in `litmap.sources`
- new embedders in `litmap.embed`
- new exporters in `litmap.visualize`

The package is intentionally conservative about what it exports today so that
the computational implementation can mature behind a stable outer interface.
