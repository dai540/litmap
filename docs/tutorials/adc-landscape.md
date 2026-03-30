# Tutorial: Antibody-Drug Conjugates

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/adc-landscape.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

Antibody-drug conjugate literature naturally spans target biology, linker-payload chemistry, resistance mechanisms, and safety translation. Those are not independent silos: target biology papers often discuss heterogeneity and resistance, while linker-payload papers frequently mention tolerability, release kinetics, and clinical dose management.

That makes ADCs a strong tutorial domain for literature mapping. A useful review article should not just show that several themes exist; it should show how broad each neighborhood is, how strongly the neighborhoods overlap, and which latent axes separate payload-oriented versus clinically translational discussion.

In practice, this is exactly the kind of topic where fixed-cluster toy examples are misleading. The literature contains broad review-like documents, mixed mechanistic papers, and partially overlapping translational reports. A density-based approach is better aligned with that reality than a fixed-k partition.

## Purpose

This tutorial asks whether an ADC corpus can be mapped with an HDBSCAN-based workflow that leaves room for noise points and variable cluster sizes. The analysis is intended to resemble how a discovery or strategy team might inspect the field when trying to understand which conversations dominate the space.

The article also uses PCA diagnostics to explain why some neighborhoods are far apart in the display and why others overlap. That is crucial if the map is to support interpretation rather than simply illustration.

## Results

- Non-noise clusters discovered: 21
- Noise points: 1
- Largest non-noise cluster: 11 (Linker and payload), 250 records

## Generated artifacts

- [labels.csv](../case-studies/adc-landscape/labels.csv)
- [cluster_summary.csv](../case-studies/adc-landscape/cluster_summary.csv)
- [coords_2d.csv](../case-studies/adc-landscape/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/adc-landscape/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/adc-landscape/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/adc-landscape/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/adc-landscape/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/adc-landscape/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/adc-landscape/map_interactive.html)
