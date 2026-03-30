from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ProjectConfig:
    name: str = "demo-run"
    run_dir: str = "./runs"


@dataclass(slots=True)
class SourceConfig:
    type: str = "csv"
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DeduplicateConfig:
    enabled: bool = True
    strategy: str = "doi_or_title_year"


@dataclass(slots=True)
class CorpusConfig:
    text_fields: list[str] = field(default_factory=lambda: ["title", "abstract"])
    text_separator: str = " [SEP] "
    require_title: bool = True
    require_abstract: bool = False
    deduplicate: DeduplicateConfig = field(default_factory=DeduplicateConfig)


@dataclass(slots=True)
class EmbeddingConfig:
    provider: str = "specter2"
    model_name: str = "allenai/specter2_base"
    adapter_name: str = "allenai/specter2"
    batch_size: int = 16
    truncation: bool = True
    device: str = "auto"


@dataclass(slots=True)
class NormalizeConfig:
    method: str = "l2"
    axis: int = 1


@dataclass(slots=True)
class PCAConfig:
    n_components: int = 2
    svd_solver: str = "full"


@dataclass(slots=True)
class HDBSCANConfig:
    min_cluster_size: int | str = "auto"
    min_cluster_size_floor: int = 15
    min_cluster_size_ratio: float = 0.01
    min_samples: int | None = None
    metric: str = "euclidean"
    cluster_selection_method: str = "eom"
    prediction_data: bool = True


@dataclass(slots=True)
class AnalysisConfig:
    normalize: NormalizeConfig = field(default_factory=NormalizeConfig)
    pca_cluster: PCAConfig = field(default_factory=lambda: PCAConfig(n_components=50))
    hdbscan: HDBSCANConfig = field(default_factory=HDBSCANConfig)
    pca_plot: PCAConfig = field(default_factory=PCAConfig)


@dataclass(slots=True)
class VisualizationConfig:
    backend: str = "plotly"
    color_noise: str = "#BDBDBD"
    opacity: float = 0.7
    hover_fields: list[str] = field(
        default_factory=lambda: ["title", "record_id", "year", "cluster", "probability"]
    )
    output_html: str = "map_interactive.html"


@dataclass(slots=True)
class OutputConfig:
    save_intermediate: bool = True
    save_manifest: bool = True
    save_environment: bool = True


@dataclass(slots=True)
class RuntimeConfig:
    random_seed: int = 42
    log_level: str = "INFO"
    resume: bool = True


@dataclass(slots=True)
class LitmapConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    source: SourceConfig = field(default_factory=SourceConfig)
    corpus: CorpusConfig = field(default_factory=CorpusConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
