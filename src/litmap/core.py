"""Small public helpers for the package."""

from __future__ import annotations


def package_overview() -> dict[str, str]:
    """Return a compact description of the package."""
    return {
        "name": "litmap",
        "purpose": "Minimal package for reproducible literature mapping.",
        "design_rule": "Cluster in analysis space, then project into display space.",
    }


def recommended_run_layout() -> tuple[str, ...]:
    """Return the recommended run directory structure."""
    return (
        "runs/",
        "  my-topic/",
        "    manifest.json",
        "    raw/",
        "    analysis/",
        "    reports/",
    )
