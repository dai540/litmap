# litmap

```{toctree}
:maxdepth: 2
:hidden:

getting-started
design
api
tutorials/index
```

```{raw} html
<div class="hero-copy">
```

`litmap` is a Python package for reproducible literature mapping.
It organizes one run as a canonical paper table, an analysis-space clustering workflow, a separate display-space projection, and a set of review-ready artifacts that remain understandable after the run is over.

The package is for workflows where a scatter plot is not enough on its own. You also want labels, summaries, diagnostics, coordinates, manifests, and a stable output layout that can be shared and revisited later.

```{raw} html
</div>
```

```{admonition} Tutorials
:class: note

Long-form case studies with cluster maps, PCA diagnostics, summary tables, and review-oriented interpretation.
[Open Tutorials](tutorials/index.md)
```

```{admonition} Getting started
:class: note

Installation, CLI entry points, and the expected run layout.
[Open Getting started](getting-started.md)
```

```{admonition} API
:class: note

The public Python surface that package users should rely on.
[Open API](api.md)
```

```{admonition} Design
:class: note

Architecture rationale, artifact boundaries, and the separation of analysis space and display space.
[Open Design](design.md)
```

## At a glance

- **Run-oriented artifacts**
  Each analysis leaves behind a canonical directory with files such as `labels.csv`, `cluster_summary.csv`, `coords_2d.csv`, and `map_interactive.html`.
- **Two-space design**
  Cluster membership is decided in analysis space. The 2D map is produced later in a separate display space.
- **Tutorial-first docs**
  The package is documented through case-study articles, not only through short setup snippets.
- **Review-ready outputs**
  The tutorials are written to support reading order, interpretation, and follow-up decisions.

## Pipeline overview

The shortest way to understand `litmap` is to see the separation between source and corpus, analysis space, and display and review outputs.

```{figure} assets/pipeline-overview.svg
:class: pipeline-figure
:alt: litmap pipeline overview

Simple architecture for one `litmap` run.
```

## Documentation map

- [Tutorials](tutorials/index.md)
- [Getting started](getting-started.md)
- [API surface](api.md)
- [Design notes](design.md)
- [Repository](https://github.com/dai540/litmap)

## Current status

```{admonition} Current status
:class: note

Best current reading path: start with a tutorial article, then move to the design notes and API.

The package surface and documentation are ahead of the final computational backend. `litmap` should currently be understood as a strong package and documentation scaffold with deterministic tutorial pipelines while the full backend continues to mature.
```
