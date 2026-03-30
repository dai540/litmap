# Tutorial: Cancer Immunotherapy

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/cancer-immunotherapy.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

Cancer immunotherapy is a good example of a literature domain that looks unified from a distance and highly heterogeneous up close. Checkpoint-response biomarkers, tissue-level immune profiling, rational combination strategy, and immune-related toxicity management all belong to the same broad field, but they answer different scientific and strategic questions.

That heterogeneity matters in pharmaceutical work because a review team is rarely trying to answer only one question. A search on immunotherapy usually serves multiple downstream needs at the same time: translational biomarker planning, indication strategy, combination positioning, safety surveillance, or competitive landscaping. A useful map should therefore preserve the fact that the field contains neighboring but non-identical neighborhoods.

A second reason this topic is useful is that overlap is not a nuisance here; it is part of the biology. Biomarker papers borrow language from microenvironment studies, combination papers reuse biomarker vocabulary, and toxicity papers still sit adjacent to treatment optimization. If the map looks perfectly segmented, it is often a sign that the analytical setup is oversimplifying the underlying literature.

## Purpose

The purpose of this tutorial is to show a literature analysis that is closer to the original design goal: normalize the embedding space, reduce it for clustering, let HDBSCAN discover cluster structure, and then separately build a 2D display space. The intention is not to force a fixed number of subfields, but to ask what structure emerges when cluster count is allowed to vary.

This also turns the tutorial into a better analytical article. Instead of ending at a decorative scatter plot, the article can discuss cluster count, noise points, PCA explained variance, component-level separation, and the interpretive gap between the clustering space and the display space.

## Results

- Non-noise clusters discovered: 22
- Noise points: 0
- Largest non-noise cluster: 22 (Bridge: Microenvironment profiling x Combination strategy), 250 records

## Generated artifacts

- [labels.csv](../case-studies/cancer-immunotherapy/labels.csv)
- [cluster_summary.csv](../case-studies/cancer-immunotherapy/cluster_summary.csv)
- [coords_2d.csv](../case-studies/cancer-immunotherapy/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/cancer-immunotherapy/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/cancer-immunotherapy/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/cancer-immunotherapy/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/cancer-immunotherapy/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/cancer-immunotherapy/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/cancer-immunotherapy/map_interactive.html)
