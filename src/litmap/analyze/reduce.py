from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

from litmap.domain.results import PipelineStep


@dataclass(slots=True)
class PCAProjection:
    coordinates: np.ndarray
    model: PCA
    explained_variance_ratio: np.ndarray


def describe_reduce_stages() -> list[PipelineStep]:
    return [
        PipelineStep(
            name="pca-cluster",
            purpose="Project normalized embeddings into the analysis space used for clustering.",
            outputs=["pca50.npy", "pca_cluster_components.csv"],
        ),
        PipelineStep(
            name="pca-plot",
            purpose="Project normalized embeddings into a 2D display space for the map.",
            outputs=["coords_2d.csv", "pca_plot_components.csv"],
        ),
    ]


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    return normalize(matrix, norm="l2", axis=1)


def run_pca(matrix: np.ndarray, n_components: int, svd_solver: str = "full") -> PCAProjection:
    model = PCA(n_components=n_components, svd_solver=svd_solver)
    coordinates = model.fit_transform(matrix)
    return PCAProjection(
        coordinates=coordinates,
        model=model,
        explained_variance_ratio=model.explained_variance_ratio_,
    )
