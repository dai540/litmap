from __future__ import annotations

from .base import BaseSource


def available_sources() -> list[BaseSource]:
    return [
        BaseSource("csv", "Load literature records from a local CSV table."),
        BaseSource("jsonl", "Load literature records from newline-delimited JSON."),
        BaseSource("pubmed", "Fetch records from PubMed via Entrez."),
        BaseSource("openalex", "Fetch records from the OpenAlex API."),
        BaseSource("semanticscholar", "Fetch records from Semantic Scholar."),
    ]
