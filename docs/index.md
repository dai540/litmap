# litmap

```{toctree}
:maxdepth: 2
:hidden:

getting-started/index
guides/index
tutorials/index
reference/index
```

`litmap` is a minimal Python package for reproducible literature mapping.
This documentation is intentionally small and keeps only the sections required to explain the package clearly.

## Sections

- [Getting Started](getting-started/index.md)
- [Guides](guides/index.md)
- [Tutorials](tutorials/index.md)
- [Reference](reference/index.md)

## Core rule

Cluster structure belongs to analysis space.
The final map belongs to display space.

```{figure} assets/pipeline-overview.svg
:alt: litmap pipeline overview

Minimal architecture for the package.
```

## Repository policy

This repository intentionally excludes large bundled data, generated tarballs, temporary directories, and bulky example outputs.
