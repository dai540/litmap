from __future__ import annotations


def recommended_layout() -> dict[str, list[str]]:
    return {
        "root": ["manifest.json", "config.snapshot.yaml"],
        "raw": ["source_query.txt", "source_records.parquet"],
        "corpus": ["papers.parquet", "text_inputs.csv", "dedup_report.csv"],
        "embeddings": ["embeddings.npy", "embeddings_l2.npy"],
        "analysis": ["pca50.npy", "labels.csv", "cluster_summary.csv", "coords_2d.csv"],
        "reports": ["map_interactive.html"],
    }


def render_layout_tree() -> str:
    return """runs/
  <run_name>/
    manifest.json
    config.snapshot.yaml
    raw/
      source_query.txt
      source_records.parquet
    corpus/
      papers.parquet
      text_inputs.csv
      dedup_report.csv
    embeddings/
      embeddings.npy
      embeddings_l2.npy
    analysis/
      pca50.npy
      labels.csv
      cluster_summary.csv
      coords_2d.csv
    reports/
      map_interactive.html"""
