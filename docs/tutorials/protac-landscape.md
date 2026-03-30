# Tutorial: PROTAC

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/protac-landscape.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

PROTAC literature mixes degrader chemistry, ligase selection, ternary-complex reasoning, and PK translation. Those topics are connected by shared degrader language, but they are not interchangeable. A map should therefore expose both the common vocabulary of the modality and the specialized substructures inside it.

This is analytically useful because PROTAC review work often alternates between chemistry-heavy and translation-heavy questions. Some teams care about linker and warhead design, others about ligase context, oral exposure, or selectivity logic. The same search set may need to serve all of those needs.

That makes PROTACs another topic where density-based clustering is preferable to a forced partition. Some records are prototypical and dense, while others are cross-cutting and may be better treated as border points or noise.

## Purpose

The purpose of this article is to rewrite the PROTAC tutorial as an HDBSCAN-centered case study and to stop pretending that a fixed cluster count is analytically natural. The output should let us describe cluster number, cluster stability, and the spread of ambiguous papers.

The article also aims to make PCA interpretation explicit. A map is easier to trust when we can say which principal components separate chemistry-oriented neighborhoods from translational neighborhoods and how much variance those axes explain.

## Results

- Non-noise clusters discovered: 23
- Noise points: 0
- Largest non-noise cluster: 22 (Bridge: Ligase biology x Ternary complex), 250 records

## Generated artifacts

- [labels.csv](../case-studies/protac-landscape/labels.csv)
- [cluster_summary.csv](../case-studies/protac-landscape/cluster_summary.csv)
- [coords_2d.csv](../case-studies/protac-landscape/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/protac-landscape/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/protac-landscape/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/protac-landscape/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/protac-landscape/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/protac-landscape/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/protac-landscape/map_interactive.html)
