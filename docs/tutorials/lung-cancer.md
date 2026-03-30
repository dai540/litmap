# Tutorial: Lung Cancer

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/lung-cancer.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

Lung cancer literature is broad enough that a single search can span classic targeted resistance, KRAS-pathway development, immunotherapy biomarkers, and plasma-based monitoring. These are related but distinct conversations, and their overlap is strategically important.

This breadth makes lung cancer a strong test case for literature mapping. It is easy to obtain a corpus that looks crowded and difficult to interpret in list form, but it is much harder to build a map that preserves both the separations and the bridges in a way that can be explained.

As in the other tutorials, a fixed cluster count would be an artificial simplification. Some neighborhoods are expected to be dense and coherent, while others should remain fuzzy because real papers often connect therapy, biomarker, and monitoring language.

## Purpose

The purpose of this tutorial is to rebuild the lung-cancer example around HDBSCAN so that cluster number, cluster size, and noise are all empirical outputs. The article then uses PCA summaries to show what is actually driving the separation seen in the map.

That makes the tutorial more useful for readers who want a review article rather than only a software demo. It becomes possible to discuss not just where papers sit, but why those patterns appear.

## Results

- Non-noise clusters discovered: 22
- Noise points: 0
- Largest non-noise cluster: 18 (Immunotherapy biomarkers), 250 records

## Generated artifacts

- [labels.csv](../case-studies/lung-cancer/labels.csv)
- [cluster_summary.csv](../case-studies/lung-cancer/cluster_summary.csv)
- [coords_2d.csv](../case-studies/lung-cancer/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/lung-cancer/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/lung-cancer/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/lung-cancer/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/lung-cancer/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/lung-cancer/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/lung-cancer/map_interactive.html)
