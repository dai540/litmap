# litmap

`litmap` is a Python package for reproducible literature mapping.
It is designed around a simple idea:

- define a corpus
- prepare normalized paper records
- build embeddings
- cluster in analysis space
- project into a separate 2D display space

The HTML docs home mirrors that same idea and adds a site map for tutorials,
API references, design notes, and the repository itself.

## Start here

- [Tutorials](tutorials/index.md): topic-focused case-study articles with concrete outputs
- [Getting started](getting-started.md): installation, commands, and package layout
- [API surface](api.md): the stable public Python interface
- [Design notes](design.md): architecture principles and run semantics
- [GitHub repository](https://github.com/dai540/litmap): source, issues, and development history

## Main outputs

A run is expected to leave behind inspectable artifacts such as:

- `labels.csv`
- `cluster_summary.csv`
- `coords_2d.csv`
- `map_interactive.html`

## Architecture overview

The HTML docs include a visual overview of the pipeline:

- [Pipeline overview chart](assets/pipeline-overview.svg)

The key design rule is that **analysis space** and **display space** stay
separate. Cluster membership is decided in the analysis pipeline; the 2D map is
only the readable projection.
