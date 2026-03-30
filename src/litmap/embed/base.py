from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EmbedderSpec:
    provider: str
    model_name: str
    description: str
