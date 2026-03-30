from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import hdbscan
import numpy as np

from litmap.config.models import HDBSCANConfig
from litmap.domain.results import PipelineStep


@dataclass(slots=True)
class HDBSCANResult:
    labels: np.ndarray
    probabilities: np.ndarray
    cluster_persistence: np.ndarray
    model: hdbscan.HDBSCAN


def describe_cluster_stage() -> PipelineStep:
    return PipelineStep(
        name="cluster",
        purpose="Run density-based clustering in the analysis space and summarize clusters.",
        outputs=[
            "labels.csv",
            "cluster_summary.csv",
            "cluster_component_profile.csv",
            "component_cluster_contrast.csv",
        ],
    )


def resolve_min_cluster_size(n_records: int, config: HDBSCANConfig) -> int:
    if isinstance(config.min_cluster_size, int):
        return config.min_cluster_size
    auto_size = ceil(config.min_cluster_size_ratio * n_records)
    return max(config.min_cluster_size_floor, auto_size)


def run_hdbscan(matrix: np.ndarray, config: HDBSCANConfig) -> HDBSCANResult:
    min_cluster_size = resolve_min_cluster_size(len(matrix), config)
    model = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=config.min_samples,
        metric=config.metric,
        cluster_selection_method=config.cluster_selection_method,
        prediction_data=config.prediction_data,
    )
    labels = model.fit_predict(matrix)
    return HDBSCANResult(
        labels=labels,
        probabilities=model.probabilities_,
        cluster_persistence=model.cluster_persistence_,
        model=model,
    )
