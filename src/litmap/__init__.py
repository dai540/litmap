"""Minimal public interface for litmap."""

from .core import package_overview, recommended_run_layout
from .version import __version__

__all__ = ["__version__", "package_overview", "recommended_run_layout"]
