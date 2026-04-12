# litmap

<img src="docs/assets/litmap-logo.svg" alt="litmap logo" width="420" />

[![Docs](https://img.shields.io/badge/docs-github.io-0f6c63)](https://dai540.github.io/litmap/)
![Python](https://img.shields.io/badge/python-3.10%2B-3776ab)
![License](https://img.shields.io/badge/license-MIT-0f172a)
![Status](https://img.shields.io/badge/status-alpha-b65a2a)

`litmap` is a minimal Python package for reproducible literature mapping.
This repository is intentionally small. It keeps only the files required to install the package, document the package with Sphinx, and explain a lightweight workflow that does not depend on large downloaded datasets.

## Scope

The package is deliberately narrow.

- It defines a minimal public API.
- It exposes a small CLI.
- It documents a run layout for literature mapping work.
- It ships a Sphinx documentation site with the four required sections:
  Getting Started, Guides, Tutorials, and Reference.

It does **not** ship large corpora, generated benchmark artifacts, virtual environments, package build tarballs, temporary directories, or heavy demo assets.

## Design constraints

This repository was rebuilt under the following constraints.

1. Keep the package installable.
2. Keep the directory tree small.
3. Keep only required source files, documentation source, and deployment files.
4. Avoid bundled data that materially increases repository size.
5. Prefer clear documentation over large example outputs.

## Installation

Install the package itself:

```bash
pip install -e .
```

Install the documentation toolchain:

```bash
pip install -e .[docs]
```

## Minimal public API

The package intentionally exports a very small interface.

- `litmap.__version__`
- `litmap.package_overview()`
- `litmap.recommended_run_layout()`

These are enough to explain what the package is for and what a run is expected to produce, without pretending that a large backend is already part of the package.

## Command line interface

The CLI is intentionally minimal.

```bash
litmap version
litmap about
litmap layout
```

- `version` prints the installed package version.
- `about` prints a compact description of the package.
- `layout` prints the recommended run directory structure.

## Recommended run layout

```text
runs/
  my-topic/
    manifest.json
    raw/
    analysis/
    reports/
```

This is documented as a contract, not as a promise that the repository already contains a full production pipeline.

## Documentation

The documentation site is built with Sphinx and is intended to be the main reading surface.

- Home
- Getting Started
- Guides
- Tutorials
- Reference

Build the documentation locally:

```bash
sphinx-build -b html docs docs/_build/html
```

## Documentation structure

The docs are intentionally lightweight.

- **Getting Started** explains installation, the CLI, and the minimal run layout.
- **Guides** explains the design principles and the intended engineering boundaries.
- **Tutorials** provides a tiny no-download toy example so the package can be understood without shipping large assets.
- **Reference** documents the public API and CLI.

## Lightweight tutorial policy

The tutorial content avoids large downloads and avoids shipping heavy generated artifacts.
The example analysis in the docs uses a tiny in-memory corpus defined directly in the article. That keeps the repository compliant with the size constraints while still making the package concrete.

## Repository contents

This repository now keeps only:

- package metadata
- package source
- Sphinx source
- lightweight SVG assets
- GitHub Pages deployment workflow

Everything else that was not required for the package itself was removed.

## Author

Author: **Dai**
