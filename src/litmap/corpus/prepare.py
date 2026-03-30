from __future__ import annotations

from litmap.domain.results import PipelineStep


def describe_corpus_stage() -> PipelineStep:
    return PipelineStep(
        name="prepare",
        purpose="Normalize source records into a stable analysis corpus.",
        outputs=["papers.parquet", "text_inputs.csv", "dedup_report.csv"],
    )
