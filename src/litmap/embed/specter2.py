from __future__ import annotations

from .base import EmbedderSpec


def describe_embedder() -> EmbedderSpec:
    return EmbedderSpec(
        provider="specter2",
        model_name="allenai/specter2_base + allenai/specter2",
        description="Scientific-paper embedding backend intended for title and abstract input.",
    )
