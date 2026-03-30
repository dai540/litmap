from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    AnalysisConfig,
    CorpusConfig,
    DeduplicateConfig,
    EmbeddingConfig,
    HDBSCANConfig,
    LitmapConfig,
    NormalizeConfig,
    OutputConfig,
    PCAConfig,
    ProjectConfig,
    RuntimeConfig,
    SourceConfig,
    VisualizationConfig,
)


def _read_mapping(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "YAML config support requires PyYAML. Install with `pip install litmap[yaml]`."
            ) from exc
        data = yaml.safe_load(text)
        return data or {}
    raise ValueError(f"Unsupported config format: {path.suffix}")


def load_config(path: str | Path) -> LitmapConfig:
    payload = _read_mapping(Path(path))

    project = ProjectConfig(**payload.get("project", {}))
    source = SourceConfig(**payload.get("source", {}))

    corpus_payload = payload.get("corpus", {})
    dedup = DeduplicateConfig(**corpus_payload.get("deduplicate", {}))
    corpus = CorpusConfig(
        text_fields=corpus_payload.get("text_fields", ["title", "abstract"]),
        text_separator=corpus_payload.get("text_separator", " [SEP] "),
        require_title=corpus_payload.get("require_title", True),
        require_abstract=corpus_payload.get("require_abstract", False),
        deduplicate=dedup,
    )

    embedding = EmbeddingConfig(**payload.get("embedding", {}))

    analysis_payload = payload.get("analysis", {})
    normalize = NormalizeConfig(**analysis_payload.get("normalize", {}))
    pca_cluster = PCAConfig(**analysis_payload.get("pca_cluster", {"n_components": 50}))
    hdbscan = HDBSCANConfig(**analysis_payload.get("hdbscan", {}))
    pca_plot = PCAConfig(**analysis_payload.get("pca_plot", {"n_components": 2}))
    analysis = AnalysisConfig(
        normalize=normalize,
        pca_cluster=pca_cluster,
        hdbscan=hdbscan,
        pca_plot=pca_plot,
    )

    visualization = VisualizationConfig(**payload.get("visualization", {}))
    output = OutputConfig(**payload.get("output", {}))
    runtime = RuntimeConfig(**payload.get("runtime", {}))

    return LitmapConfig(
        project=project,
        source=source,
        corpus=corpus,
        embedding=embedding,
        analysis=analysis,
        visualization=visualization,
        output=output,
        runtime=runtime,
    )
