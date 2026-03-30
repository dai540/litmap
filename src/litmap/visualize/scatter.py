from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from litmap.domain.results import PipelineStep


def describe_visualization_stage() -> PipelineStep:
    return PipelineStep(
        name="map",
        purpose="Render an interactive literature map from 2D coordinates and cluster labels.",
        outputs=["map_interactive.html", "map_static.html"],
    )


def build_plotly_map(
    table: pd.DataFrame,
    title: str,
    opacity: float = 0.68,
    noise_color: str = "#BDBDBD",
) -> go.Figure:
    frame = table.copy()
    if "cluster_display" not in frame.columns:
        frame["cluster_display"] = frame["cluster"].astype(str)
    ordered = [value for value in frame["cluster_display"].drop_duplicates().tolist() if value != "Noise"]
    ordered = sorted(ordered, key=lambda value: int(str(value).replace("Cluster ", "")))
    if "Noise" in set(frame["cluster_display"]):
        ordered.append("Noise")
    palette = px.colors.qualitative.Safe + px.colors.qualitative.Vivid + px.colors.qualitative.Bold
    color_map: dict[str, str] = {}
    palette_index = 0
    for cluster_id in ordered:
        if cluster_id == "Noise":
            color_map[cluster_id] = noise_color
            continue
        color_map[cluster_id] = palette[palette_index % len(palette)]
        palette_index += 1

    figure = px.scatter(
        frame,
        x="pc1_plot",
        y="pc2_plot",
        color="cluster_display",
        hover_data={
            "title": True,
            "record_id": True,
            "year": True,
            "cluster": True,
            "original_cluster_id": True if "original_cluster_id" in frame.columns else False,
            "probability": ":.3f",
            "pc1_plot": ":.3f",
            "pc2_plot": ":.3f",
        },
        color_discrete_map=color_map,
        category_orders={"cluster_display": ordered},
        title=title,
        labels={
            "pc1_plot": "PC1",
            "pc2_plot": "PC2",
            "cluster_display": "Cluster",
        },
    )
    figure.update_traces(marker={"size": 7, "opacity": opacity, "line": {"width": 0}})
    figure.update_layout(
        template="plotly_white",
        legend={
            "title": {"text": "Cluster"},
            "x": 1.02,
            "y": 1.0,
            "xanchor": "left",
            "yanchor": "top",
            "bgcolor": "rgba(255,255,255,0.88)",
            "bordercolor": "rgba(120,120,120,0.28)",
            "borderwidth": 1,
        },
        margin={"l": 80, "r": 260, "t": 70, "b": 80},
    )
    figure.update_xaxes(title_text="PC1", showgrid=True, zeroline=False)
    figure.update_yaxes(title_text="PC2", showgrid=True, zeroline=False)
    return figure


def write_plotly_html(figure: go.Figure, path: Path) -> None:
    figure.write_html(str(path), include_plotlyjs="cdn", full_html=True)
