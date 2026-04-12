# Toy corpus tutorial

This tutorial shows the intended idea of `litmap` without bundling real corpora.

## Goal

Use a tiny literature-like corpus to explain the difference between analysis space and display space.

## Example corpus

```python
papers = [
    {"id": "P1", "title": "Checkpoint blockade biomarkers", "abstract": "PD-L1 and T cell infiltration"},
    {"id": "P2", "title": "Tumor microenvironment profiling", "abstract": "macrophage and stromal context"},
    {"id": "P3", "title": "ADC linker payload strategy", "abstract": "linker stability and payload release"},
]
```

## Interpretation

Even in a toy corpus, the package should keep the conceptual rule clear:

- the analytical representation decides what is near what
- the plotting representation exists only to make the result readable

This tutorial stops at the conceptual level on purpose. That keeps the repository small and avoids shipping heavy artifacts.
