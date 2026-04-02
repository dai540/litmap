# Design

## Core idea

`litmap` is built around one central distinction:

- **analysis space** determines cluster membership
- **display space** determines how the result is shown on a map

That rule keeps a visually pleasing map from silently redefining the underlying cluster structure.

## Architectural layers

1. `sources`
   ingest external records from PubMed, OpenAlex, Semantic Scholar, or local files
2. `corpus`
   normalize metadata, build embedding input text, and deduplicate records
3. `embed`
   generate literature embeddings
4. `analyze`
   normalize, reduce, cluster, and summarize
5. `visualize`
   export interactive maps and shareable figures
6. `storage`
   define the artifact contract for runs
7. `pipeline`
   orchestrate the stages

## Run naming

Run directories should use human-readable names such as:

- `immunotherapy-landscape`
- `glioma-methods-scan`
- `single-cell-review`

Timestamps should not be part of the primary run name.

## Why the docs are case-study oriented

A package like `litmap` is easier to trust when the documentation shows the shapes of real outputs. That is why the tutorials are written around result artifacts rather than only around setup commands.
