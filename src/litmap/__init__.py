"""Public package interface for litmap."""

from .config.loader import load_config
from .config.models import LitmapConfig
from .pipeline.runner import describe_pipeline, run_pipeline
from .version import __version__

__all__ = [
    "LitmapConfig",
    "__version__",
    "describe_pipeline",
    "load_config",
    "run_pipeline",
]
