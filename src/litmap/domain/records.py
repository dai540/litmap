from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PaperRecord:
    record_id: str
    source: str
    source_id: str
    title: str
    abstract: str = ""
    year: int | None = None
    venue: str | None = None
    doi: str | None = None
    url: str | None = None
