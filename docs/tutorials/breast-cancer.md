# Tutorial: Breast Cancer

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/breast-cancer.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

Breast cancer literature is heterogeneous by design. HER2-directed development, endocrine resistance, triple-negative immunotherapy, and ctDNA or MRD monitoring sit inside the same clinical area but reflect different translational priorities and different scientific vocabularies.

That makes breast cancer a useful test of whether the map can capture clinically meaningful structure without collapsing everything into subtype labels. Real review work often spans modalities, biomarkers, and monitoring approaches at the same time.

A map that is too tidy risks erasing the fact that HER2 papers borrow resistance language, endocrine papers overlap with biomarker discussion, and MRD monitoring papers often connect back to treatment adaptation.

## Purpose

This tutorial aims to build a broader breast-cancer literature landscape with density-based clustering, not a fixed-k partition. The goal is to see which subfields emerge as dense neighborhoods and which documents remain ambiguous or diffuse.

The article also uses PCA diagnostics to ground interpretation. Instead of simply declaring what a cluster means, we inspect which axes of variation separate the main neighborhoods and how much of the structure is carried by the displayed dimensions.

## Results

- Non-noise clusters discovered: 20
- Noise points: 10
- Largest non-noise cluster: 4 (Review hub: HER2 antibody combinations x ESR1 mutations), 250 records

## Generated artifacts

- [labels.csv](../case-studies/breast-cancer/labels.csv)
- [cluster_summary.csv](../case-studies/breast-cancer/cluster_summary.csv)
- [coords_2d.csv](../case-studies/breast-cancer/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/breast-cancer/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/breast-cancer/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/breast-cancer/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/breast-cancer/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/breast-cancer/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/breast-cancer/map_interactive.html)
