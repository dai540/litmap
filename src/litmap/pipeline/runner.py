from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from litmap.analyze import describe_cluster_stage, describe_reduce_stages
from litmap.config.models import LitmapConfig
from litmap.corpus import describe_corpus_stage
from litmap.domain.results import PipelineStep, RunResult
from litmap.storage import render_layout_tree
from litmap.visualize import describe_visualization_stage


def describe_pipeline(config: LitmapConfig) -> list[PipelineStep]:
    return [
        PipelineStep(
            name="ingest",
            purpose=f"Collect records from source `{config.source.type}`.",
            outputs=["source_records.parquet"],
        ),
        describe_corpus_stage(),
        PipelineStep(
            name="embed",
            purpose=f"Embed prepared literature records with `{config.embedding.provider}`.",
            outputs=["embeddings.npy", "embeddings_l2.npy"],
        ),
        *describe_reduce_stages(),
        describe_cluster_stage(),
        describe_visualization_stage(),
    ]


def run_pipeline(config: LitmapConfig, run_dir: str | None = None) -> RunResult:
    root = Path(run_dir or config.project.run_dir)
    run_id = f"{config.project.name}-{uuid4().hex[:8]}"
    run_path = root / run_id
    summary = (
        "Scaffold run created under a stable, human-readable run name. "
        "Analytical execution is not implemented yet; use this object to inspect "
        "the intended pipeline and output layout.\n\n"
        + render_layout_tree()
    )
    return RunResult(
        run_id=run_id,
        run_path=str(run_path),
        summary=summary,
        steps=describe_pipeline(config),
    )
