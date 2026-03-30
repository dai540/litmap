from __future__ import annotations

import json
import math
import random
import site
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, site.getusersitepackages())
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
import pandas as pd

from litmap.analyze.cluster import run_hdbscan
from litmap.analyze.reduce import l2_normalize, run_pca
from litmap.config.models import HDBSCANConfig
from litmap.embed.tfidf import build_tfidf_embeddings
from litmap.visualize.scatter import build_plotly_map, write_plotly_html

DOCS = ROOT / "docs"
DATA_DIR = DOCS / "tutorial-data"
CASE_DIR = DOCS / "case-studies"
TUTORIAL_DIR = DOCS / "tutorials"

SHARED_TERMS = [
    "patient stratification",
    "translational biomarker",
    "dose optimization",
    "mechanism of resistance",
    "clinical development",
    "validation cohort",
    "early-phase trial",
    "real-world evidence",
    "molecular profiling",
    "portfolio review",
]


@dataclass(frozen=True)
class ThemeSeed:
    label: str
    title_prefix: str
    title_topics: list[str]
    abstract_terms: list[str]


@dataclass(frozen=True)
class StudySpec:
    slug: str
    title: str
    background: list[str]
    purpose: list[str]
    interpretation: list[str]
    themes: list[ThemeSeed]
    total_records: int = 3000


STUDIES = [
    StudySpec(
        slug="cancer-immunotherapy",
        title="Cancer Immunotherapy",
        background=[
            "Cancer immunotherapy is a good example of a literature domain that looks unified from a distance and highly heterogeneous up close. Checkpoint-response biomarkers, tissue-level immune profiling, rational combination strategy, and immune-related toxicity management all belong to the same broad field, but they answer different scientific and strategic questions.",
            "That heterogeneity matters in pharmaceutical work because a review team is rarely trying to answer only one question. A search on immunotherapy usually serves multiple downstream needs at the same time: translational biomarker planning, indication strategy, combination positioning, safety surveillance, or competitive landscaping. A useful map should therefore preserve the fact that the field contains neighboring but non-identical neighborhoods.",
            "A second reason this topic is useful is that overlap is not a nuisance here; it is part of the biology. Biomarker papers borrow language from microenvironment studies, combination papers reuse biomarker vocabulary, and toxicity papers still sit adjacent to treatment optimization. If the map looks perfectly segmented, it is often a sign that the analytical setup is oversimplifying the underlying literature.",
        ],
        purpose=[
            "The purpose of this tutorial is to show a literature analysis that is closer to the original design goal: normalize the embedding space, reduce it for clustering, let HDBSCAN discover cluster structure, and then separately build a 2D display space. The intention is not to force a fixed number of subfields, but to ask what structure emerges when cluster count is allowed to vary.",
            "This also turns the tutorial into a better analytical article. Instead of ending at a decorative scatter plot, the article can discuss cluster count, noise points, PCA explained variance, component-level separation, and the interpretive gap between the clustering space and the display space.",
        ],
        interpretation=[
            "The resulting immunotherapy map should be read as a portfolio-level reading aid rather than a hard taxonomy. Large neighborhoods may represent broad themes such as biomarker-driven review papers or mixed clinical strategy papers, while smaller neighborhoods often reflect more specific and technically coherent slices of the field.",
            "What matters is not whether the output is visually neat, but whether the map plus its tables support an explainable review narrative: which parts of the field dominate, which themes overlap, and which axes of variance are actually driving the observed structure.",
        ],
        themes=[
            ThemeSeed("Checkpoint biomarkers", "Biomarker mapping for", ["PD-1 response", "PD-L1 scoring", "interferon-gamma signatures", "T-cell exhaustion"], ["checkpoint blockade", "response stratification", "interferon signaling", "selection biomarker", "immune exclusion", "predictive assay"]),
            ThemeSeed("Microenvironment profiling", "Spatial and single-cell profiling of", ["immune niches", "macrophage barriers", "lymphocyte states", "tumor microenvironment"], ["spatial atlas", "single-cell profiling", "myeloid state", "tissue architecture", "stromal barrier", "immune contexture"]),
            ThemeSeed("Combination strategy", "Combination immunotherapy strategy in", ["VEGF blockade", "radiotherapy priming", "neoantigen vaccination", "bispecific activation"], ["combination regimen", "synergy signal", "treatment sequence", "priming effect", "vaccine strategy", "adaptive resistance"]),
            ThemeSeed("Toxicity management", "Management of immune-related", ["colitis", "myocarditis", "pneumonitis", "endocrinopathies"], ["safety monitoring", "steroid management", "immune-related adverse event", "toxicity grading", "clinical triage", "rechallenge strategy"]),
        ],
    ),
    StudySpec(
        slug="adc-landscape",
        title="Antibody-Drug Conjugates",
        background=[
            "Antibody-drug conjugate literature naturally spans target biology, linker-payload chemistry, resistance mechanisms, and safety translation. Those are not independent silos: target biology papers often discuss heterogeneity and resistance, while linker-payload papers frequently mention tolerability, release kinetics, and clinical dose management.",
            "That makes ADCs a strong tutorial domain for literature mapping. A useful review article should not just show that several themes exist; it should show how broad each neighborhood is, how strongly the neighborhoods overlap, and which latent axes separate payload-oriented versus clinically translational discussion.",
            "In practice, this is exactly the kind of topic where fixed-cluster toy examples are misleading. The literature contains broad review-like documents, mixed mechanistic papers, and partially overlapping translational reports. A density-based approach is better aligned with that reality than a fixed-k partition.",
        ],
        purpose=[
            "This tutorial asks whether an ADC corpus can be mapped with an HDBSCAN-based workflow that leaves room for noise points and variable cluster sizes. The analysis is intended to resemble how a discovery or strategy team might inspect the field when trying to understand which conversations dominate the space.",
            "The article also uses PCA diagnostics to explain why some neighborhoods are far apart in the display and why others overlap. That is crucial if the map is to support interpretation rather than simply illustration.",
        ],
        interpretation=[
            "A good ADC map should reveal both dominant topics and bridges. One would expect to see chemistry-heavy and safety-heavy regions, but also papers that connect target biology to resistance or conjugation design to translational dose considerations.",
            "If the map shows a broad diffuse region, that should not immediately be treated as a flaw. In a real corpus, diffuse regions often correspond to umbrella review language or mixed-theme translational papers, and those are often strategically important.",
        ],
        themes=[
            ThemeSeed("Target biology", "Target biology for", ["HER2 ADCs", "TROP2 programs", "HER3 targeting", "LIV1 selection"], ["target expression", "surface biology", "internalization", "antigen density", "selection rationale", "tumor heterogeneity"]),
            ThemeSeed("Linker and payload", "Linker-payload optimization for", ["topoisomerase payloads", "tubulin payloads", "cleavable linkers", "site-specific conjugation"], ["linker stability", "payload release", "conjugation chemistry", "drug-antibody ratio", "bystander payload", "site-specific linker"]),
            ThemeSeed("Resistance and bystander", "Resistance mechanisms in", ["antigen loss", "bystander effect", "payload efflux", "lysosomal processing"], ["resistance biology", "bystander killing", "payload efflux", "lysosomal escape", "heterogeneity signal", "processing defect"]),
            ThemeSeed("Safety translation", "Clinical safety translation of", ["interstitial lung disease", "ocular toxicity", "hematologic toxicity", "dose optimization"], ["safety signal", "dose reduction", "clinical monitoring", "translation risk", "hematologic toxicity", "lung toxicity"]),
        ],
    ),
    StudySpec(
        slug="protac-landscape",
        title="PROTAC",
        background=[
            "PROTAC literature mixes degrader chemistry, ligase selection, ternary-complex reasoning, and PK translation. Those topics are connected by shared degrader language, but they are not interchangeable. A map should therefore expose both the common vocabulary of the modality and the specialized substructures inside it.",
            "This is analytically useful because PROTAC review work often alternates between chemistry-heavy and translation-heavy questions. Some teams care about linker and warhead design, others about ligase context, oral exposure, or selectivity logic. The same search set may need to serve all of those needs.",
            "That makes PROTACs another topic where density-based clustering is preferable to a forced partition. Some records are prototypical and dense, while others are cross-cutting and may be better treated as border points or noise.",
        ],
        purpose=[
            "The purpose of this article is to rewrite the PROTAC tutorial as an HDBSCAN-centered case study and to stop pretending that a fixed cluster count is analytically natural. The output should let us describe cluster number, cluster stability, and the spread of ambiguous papers.",
            "The article also aims to make PCA interpretation explicit. A map is easier to trust when we can say which principal components separate chemistry-oriented neighborhoods from translational neighborhoods and how much variance those axes explain.",
        ],
        interpretation=[
            "A useful PROTAC landscape will typically contain both compact and diffuse neighborhoods. Compact neighborhoods often correspond to technically coherent chemical or structural discussions, whereas diffuse ones tend to absorb broader translational or mixed-mechanism records.",
            "The value of the map lies in its ability to support reading and prioritization, not in pretending to produce a definitive ontology of the field.",
        ],
        themes=[
            ThemeSeed("Degrader chemistry", "Degrader design for", ["kinase targets", "transcription factors", "epigenetic regulators", "nuclear receptors"], ["warhead design", "linker chemistry", "degrader optimization", "structure-activity relationship", "chemical series", "permeability challenge"]),
            ThemeSeed("Ligase biology", "E3 ligase selection in", ["CRBN programs", "VHL recruiters", "DCAF strategies", "ligase expression profiling"], ["ligase expression", "recruiter choice", "cell context", "ligase biology", "tissue dependence", "selective degradation"]),
            ThemeSeed("Ternary complex", "Ternary complex modeling for", ["cooperativity prediction", "structural dynamics", "residence time", "degradation selectivity"], ["ternary complex", "cooperativity", "structural model", "selectivity logic", "binding geometry", "kinetic reasoning"]),
            ThemeSeed("PK and translation", "Exposure translation for", ["oral degraders", "brain-penetrant degraders", "PK-PD linkage", "human dose projection"], ["oral exposure", "PK translation", "distribution challenge", "dose projection", "brain penetration", "development path"]),
        ],
    ),
    StudySpec(
        slug="breast-cancer",
        title="Breast Cancer",
        background=[
            "Breast cancer literature is heterogeneous by design. HER2-directed development, endocrine resistance, triple-negative immunotherapy, and ctDNA or MRD monitoring sit inside the same clinical area but reflect different translational priorities and different scientific vocabularies.",
            "That makes breast cancer a useful test of whether the map can capture clinically meaningful structure without collapsing everything into subtype labels. Real review work often spans modalities, biomarkers, and monitoring approaches at the same time.",
            "A map that is too tidy risks erasing the fact that HER2 papers borrow resistance language, endocrine papers overlap with biomarker discussion, and MRD monitoring papers often connect back to treatment adaptation.",
        ],
        purpose=[
            "This tutorial aims to build a broader breast-cancer literature landscape with density-based clustering, not a fixed-k partition. The goal is to see which subfields emerge as dense neighborhoods and which documents remain ambiguous or diffuse.",
            "The article also uses PCA diagnostics to ground interpretation. Instead of simply declaring what a cluster means, we inspect which axes of variation separate the main neighborhoods and how much of the structure is carried by the displayed dimensions.",
        ],
        interpretation=[
            "The resulting map should be interpreted as a strategic landscape view. Some neighborhoods will correspond to clinically recognizable subfields, while others may reflect blended translational discussion across response, resistance, and monitoring.",
            "That is acceptable and often desirable, because portfolio-level reviews need to preserve adjacency as well as separation.",
        ],
        themes=[
            ThemeSeed("HER2 biology", "HER2-focused development in", ["HER2-low disease", "HER2 resistance", "brain metastases", "HER2 antibody combinations"], ["HER2 biology", "antibody development", "brain metastasis", "resistance adaptation", "amplification signal", "combination treatment"]),
            ThemeSeed("Endocrine resistance", "Endocrine resistance strategy for", ["ESR1 mutations", "CDK4/6 adaptation", "PI3K pathway", "selective estrogen degraders"], ["endocrine resistance", "ESR1 mutation", "hormone signaling", "CDK4/6 adaptation", "ER pathway", "targeted escape"]),
            ThemeSeed("TNBC immunotherapy", "Immunotherapy programs in", ["triple-negative disease", "PD-L1 stratification", "microenvironment phenotypes", "combination checkpoint blockade"], ["TNBC immune context", "checkpoint biomarker", "microenvironment state", "combination immunotherapy", "PD-L1 selection", "stromal exclusion"]),
            ThemeSeed("Monitoring and MRD", "Residual disease monitoring in", ["ctDNA surveillance", "minimal residual disease", "neoadjuvant response", "longitudinal liquid biopsy"], ["ctDNA monitoring", "minimal residual disease", "liquid biopsy", "longitudinal surveillance", "response tracking", "molecular relapse"]),
        ],
    ),
    StudySpec(
        slug="lung-cancer",
        title="Lung Cancer",
        background=[
            "Lung cancer literature is broad enough that a single search can span classic targeted resistance, KRAS-pathway development, immunotherapy biomarkers, and plasma-based monitoring. These are related but distinct conversations, and their overlap is strategically important.",
            "This breadth makes lung cancer a strong test case for literature mapping. It is easy to obtain a corpus that looks crowded and difficult to interpret in list form, but it is much harder to build a map that preserves both the separations and the bridges in a way that can be explained.",
            "As in the other tutorials, a fixed cluster count would be an artificial simplification. Some neighborhoods are expected to be dense and coherent, while others should remain fuzzy because real papers often connect therapy, biomarker, and monitoring language.",
        ],
        purpose=[
            "The purpose of this tutorial is to rebuild the lung-cancer example around HDBSCAN so that cluster number, cluster size, and noise are all empirical outputs. The article then uses PCA summaries to show what is actually driving the separation seen in the map.",
            "That makes the tutorial more useful for readers who want a review article rather than only a software demo. It becomes possible to discuss not just where papers sit, but why those patterns appear.",
        ],
        interpretation=[
            "A useful lung-cancer landscape should distinguish targeted-resistance regions, KRAS-development regions, biomarker-rich immunotherapy regions, and monitoring-heavy regions, while still leaving room for mixed or transitional records.",
            "The correct reading is therefore not a literal count of islands on the map, but a combined reading of density-based clusters, noise points, PCA contributions, and cluster profiles in principal-component space.",
        ],
        themes=[
            ThemeSeed("EGFR and ALK resistance", "Resistance evolution in", ["EGFR-mutant disease", "ALK-positive tumors", "osimertinib escape", "CNS progression"], ["EGFR resistance", "ALK progression", "targeted escape", "CNS metastasis", "line-of-therapy shift", "acquired resistance"]),
            ThemeSeed("KRAS development", "KRAS pathway development in", ["KRAS G12C inhibition", "adaptive signaling", "SHP2 combinations", "pan-KRAS strategies"], ["KRAS inhibitor", "adaptive pathway", "combination rationale", "SHP2 biology", "development strategy", "feedback signaling"]),
            ThemeSeed("Immunotherapy biomarkers", "Biomarker selection in", ["PD-L1-high tumors", "tumor mutational burden", "STK11 co-mutation", "immune exclusion"], ["PD-L1 biomarker", "tumor mutational burden", "immune exclusion", "selection logic", "co-mutation effect", "checkpoint response"]),
            ThemeSeed("ctDNA and monitoring", "Molecular monitoring for", ["ctDNA resistance tracking", "minimal residual disease", "adjuvant surveillance", "longitudinal plasma genotyping"], ["ctDNA surveillance", "plasma genotyping", "molecular monitoring", "residual disease", "longitudinal sampling", "liquid biopsy"]),
        ],
    ),
]


def generate_records(spec: StudySpec) -> pd.DataFrame:
    rng = random.Random(spec.slug)
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    n_themes = len(spec.themes)
    review_count = spec.total_records // 6
    crossover_count = spec.total_records // 6
    core_count = spec.total_records - review_count - crossover_count
    per_theme = core_count // n_themes
    rows: list[dict[str, object]] = []

    for theme_index, theme in enumerate(spec.themes):
        for i in range(per_theme):
            topic = theme.title_topics[i % len(theme.title_topics)]
            own_terms = rng.sample(theme.abstract_terms, k=3)
            neighbor = spec.themes[(theme_index + 1 + (i % (n_themes - 1))) % n_themes]
            borrowed = rng.sample(neighbor.abstract_terms, k=2)
            shared = rng.sample(SHARED_TERMS, k=2)
            rows.append(
                {
                    "record_id": f"{spec.slug}-{theme_index + 1:02d}-{i + 1:04d}",
                    "title": f"{theme.title_prefix} {topic}: study {i + 1}",
                    "abstract": (
                        f"This study examines {topic} through {own_terms[0]}, {own_terms[1]}, and {own_terms[2]}. "
                        f"It also discusses links to {borrowed[0]} and {borrowed[1]}, alongside {shared[0]} and {shared[1]}."
                    ),
                    "year": years[(theme_index + i) % len(years)],
                    "seed_theme": theme.label,
                    "record_type": "core",
                }
            )

    for i in range(crossover_count):
        left = spec.themes[i % n_themes]
        right = spec.themes[(i + 1) % n_themes]
        left_topic = left.title_topics[i % len(left.title_topics)]
        right_topic = right.title_topics[(i * 2) % len(right.title_topics)]
        left_terms = rng.sample(left.abstract_terms, k=2)
        right_terms = rng.sample(right.abstract_terms, k=2)
        shared = rng.sample(SHARED_TERMS, k=3)
        rows.append(
            {
                "record_id": f"{spec.slug}-x-{i + 1:04d}",
                "title": f"Integrated analysis of {left_topic} with {right_topic}: study {i + 1}",
                "abstract": (
                    f"This paper links {left_terms[0]} and {left_terms[1]} to {right_terms[0]} and {right_terms[1]}. "
                    f"The framing emphasizes {shared[0]}, {shared[1]}, and {shared[2]} across mixed translational contexts."
                ),
                "year": years[i % len(years)],
                "seed_theme": f"{left.label} + {right.label}",
                "record_type": "crossover",
            }
        )

    for i in range(review_count):
        topics = [theme.title_topics[(i + idx) % len(theme.title_topics)] for idx, theme in enumerate(spec.themes)]
        terms = [rng.choice(theme.abstract_terms) for theme in spec.themes]
        shared = rng.sample(SHARED_TERMS, k=4)
        rows.append(
            {
                "record_id": f"{spec.slug}-r-{i + 1:04d}",
                "title": f"Landscape review of {topics[0]}, {topics[1]}, and {topics[2]}",
                "abstract": (
                    f"This review connects {terms[0]}, {terms[1]}, {terms[2]}, and {terms[3]}. "
                    f"It frames the field around {shared[0]}, {shared[1]}, {shared[2]}, and {shared[3]}."
                ),
                "year": years[(i + 2) % len(years)],
                "seed_theme": "review-like mixed corpus",
                "record_type": "review",
            }
        )

    frame = pd.DataFrame(rows)
    return frame.sample(frac=1.0, random_state=42).reset_index(drop=True)


def resolve_cluster_label(label: int, theme_map: dict[int, str]) -> str:
    return "noise" if label == -1 else theme_map.get(label, f"cluster {label}")


def infer_cluster_themes(labels: np.ndarray, matrix: np.ndarray, vocabulary: list[str]) -> dict[int, str]:
    themes: dict[int, str] = {}
    for label in sorted(set(labels)):
        if label == -1:
            continue
        member_index = np.where(labels == label)[0]
        centroid = matrix[member_index].mean(axis=0)
        top_index = np.argsort(centroid)[::-1][:4]
        terms = [vocabulary[i].replace("_", " ") for i in top_index if centroid[i] > 0]
        themes[label] = ", ".join(terms[:3]) if terms else f"cluster {label}"
    return themes


def article_theme_name(subset: pd.DataFrame, fallback: str) -> str:
    if subset.empty:
        return fallback
    type_share = subset["record_type"].value_counts(normalize=True)
    seed_counts = subset["seed_theme"].value_counts()
    non_review_seed_counts = seed_counts.drop(labels=["review-like mixed corpus"], errors="ignore")
    dominant_seed = str(seed_counts.index[0])
    dominant_share = float(seed_counts.iloc[0] / len(subset))

    def top_non_review_labels(limit: int = 2) -> list[str]:
        if non_review_seed_counts.empty:
            return []
        return [str(label) for label in non_review_seed_counts.index[:limit]]

    def bridge_label(left: str, right: str) -> str:
        return f"Bridge: {left} x {right}"

    def review_title_label() -> str | None:
        review_titles = subset.loc[subset["record_type"] == "review", "title"]
        if review_titles.empty:
            review_titles = subset["title"]
        if review_titles.empty:
            return None
        exemplar = str(review_titles.iloc[0])
        prefix = "Landscape review of "
        if not exemplar.startswith(prefix):
            return None
        phrase = exemplar[len(prefix):].split(":", 1)[0]
        cleaned = phrase.replace(" and ", ", ")
        parts = [part.strip() for part in cleaned.split(",") if part.strip()]
        if len(parts) >= 2:
            return f"Review hub: {parts[0]} x {parts[1]}"
        if len(parts) == 1:
            return f"Review hub: {parts[0]}"
        return None

    if type_share.get("review", 0.0) >= 0.5:
        title_label = review_title_label()
        if title_label:
            return title_label
        neighbors = top_non_review_labels()
        if len(neighbors) >= 2:
            return f"Review hub: {neighbors[0]} x {neighbors[1]}"
        if len(neighbors) == 1:
            return f"Review hub: {neighbors[0]}"
        if dominant_seed == "review-like mixed corpus":
            return "Review hub: mixed field overview"
        return f"Review hub: {dominant_seed}"

    if type_share.get("crossover", 0.0) >= 0.45:
        if "+" in dominant_seed:
            left, right = [part.strip() for part in dominant_seed.split("+", 1)]
            return bridge_label(left, right)
        neighbors = top_non_review_labels()
        if len(neighbors) >= 2:
            return bridge_label(neighbors[0], neighbors[1])
        return f"Bridge: {dominant_seed}"

    if dominant_share >= 0.6:
        return dominant_seed

    if len(seed_counts) > 1:
        second_seed = str(seed_counts.index[1])
        if dominant_seed == second_seed:
            return dominant_seed
        if dominant_seed == "review-like mixed corpus":
            neighbors = top_non_review_labels()
            if len(neighbors) >= 2:
                return f"Mixed hub: {neighbors[0]} + {neighbors[1]}"
            if len(neighbors) == 1:
                return f"Mixed hub: {neighbors[0]} + review"
        return f"Mixed hub: {dominant_seed} + {second_seed}"

    return fallback


def representative_titles(table: pd.DataFrame, cluster_id: int, limit: int = 5) -> str:
    subset = table.loc[table["cluster"] == cluster_id].sort_values("probability", ascending=False)
    return " | ".join(subset["title"].head(limit).tolist())


def named_cluster_rows(cluster_summary: pd.DataFrame) -> pd.DataFrame:
    return cluster_summary.loc[cluster_summary["cluster_id"] != -1].copy().reset_index(drop=True)


def top_named_rows(frame: pd.DataFrame, by: list[str], ascending: list[bool], limit: int = 3) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()
    return frame.sort_values(by, ascending=ascending).head(limit).reset_index(drop=True)


def format_cluster_refs(
    frame: pd.DataFrame,
    include_size: bool = False,
    include_persistence: bool = False,
    include_probability: bool = False,
) -> str:
    refs: list[str] = []
    for row in frame.itertuples():
        extras: list[str] = []
        if include_size:
            extras.append(f"{int(row.size)} records")
        if include_persistence:
            extras.append(f"persistence {row.persistence_display}")
        if include_probability:
            extras.append(f"mean probability {row.mean_probability:.3f}")
        detail = ", ".join(extras)
        if detail:
            refs.append(f"Cluster {int(row.cluster_id)} ({row.theme}; {detail})")
        else:
            refs.append(f"Cluster {int(row.cluster_id)} ({row.theme})")
    return ", ".join(refs)


def interface_from_theme(theme: str) -> str:
    if theme.startswith("Bridge: "):
        return theme.removeprefix("Bridge: ").replace(" x ", " and ")
    if theme.startswith("Review hub: "):
        return theme.removeprefix("Review hub: ")
    if theme.startswith("Mixed hub: "):
        return theme.removeprefix("Mixed hub: ").replace(" + ", " and ")
    return theme


def theme_family(theme: str) -> str:
    if theme.startswith("Bridge: "):
        return "bridge"
    if theme.startswith("Review hub: "):
        return "review"
    if theme.startswith("Mixed hub: "):
        return "mixed"
    return "core"


def build_headline_findings(
    cluster_summary: pd.DataFrame,
    labels_table: pd.DataFrame,
    contrast_table: pd.DataFrame,
) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "This run is dominated by noise, so the headline finding is negative: under the current representation the corpus does not resolve into actionable dense neighborhoods."
        ]

    broad = top_named_rows(non_noise, ["size", "mean_probability"], [False, False], limit=3)
    stable = top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=2)
    bridge = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    noise_count = int((labels_table["cluster"] == -1).sum())
    total = int(len(labels_table))
    noise_ratio = noise_count / total if total else 0.0
    findings = [
        "The corpus is not flat. The largest neighborhoods are "
        + format_cluster_refs(broad, include_size=True)
        + ", which means the literature is concentrating around a small number of high-density conversations rather than scattering evenly across many tiny topics.",
        "The most defensible clusters for close reading are "
        + format_cluster_refs(stable, include_persistence=True, include_probability=True)
        + ". These are the parts of the map where density and assignment confidence align best, so they are the safest starting points for building thematic review packets.",
    ]
    if not bridge.empty:
        findings.append(
            "The most interesting clusters are not only the largest ones. Bridge-like neighborhoods such as "
            + format_cluster_refs(bridge, include_size=True)
            + " indicate that the field is generating papers at the interface between themes, which is usually where translational questions and portfolio decisions become non-trivial."
        )
    if not review.empty:
        findings.append(
            "A separate layer of the corpus is review-centered rather than mechanistically sharp. Clusters such as "
            + format_cluster_refs(review, include_size=True)
            + " are useful for orientation and synthesis, but they should not be mistaken for the densest primary-evidence pockets."
        )
    findings.append(
        f"Only {noise_count} records ({noise_ratio:.1%}) fall into noise. That means most of the corpus is being captured by recurring local structure rather than floating as one-off outliers, which makes this run suitable for structured interpretation rather than only exploratory browsing."
    )
    if not contrast_table.empty:
        first = contrast_table.iloc[0]
        findings.append(
            f"The strongest single axis of separation is {first['component']}, where Cluster {int(first['low_cluster'])} and Cluster {int(first['high_cluster'])} are the furthest apart. That matters because the map is not just partitioning by theme count; it is partitioning by a specific latent contrast that can be inspected through PCA loadings."
        )
    return findings


def build_perspective_discussion(cluster_summary: pd.DataFrame) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "Decision-wise, the immediate recommendation would be to improve corpus definition or representation before acting on the map, because the current solution does not support stable cluster-level prioritization."
        ]

    stable = non_noise.sort_values(["persistence", "size"], ascending=[False, False]).head(2).reset_index(drop=True)
    broad = non_noise.sort_values(["size", "mean_probability"], ascending=[False, False]).head(2).reset_index(drop=True)
    weak = non_noise.sort_values(["persistence", "mean_probability"], ascending=[True, True]).head(2).reset_index(drop=True)
    bridge = non_noise.loc[non_noise["theme"].str.startswith("Bridge:", na=False)].sort_values(
        ["size", "persistence"], ascending=[False, False]
    ).head(2).reset_index(drop=True)
    review = non_noise.loc[non_noise["theme"].str.startswith("Review hub:", na=False)].sort_values(
        ["size", "persistence"], ascending=[False, False]
    ).head(2).reset_index(drop=True)

    paragraphs = [
        "One practical use of this result is triage. The most stable clusters are good candidates for focused review packets or owner-based deep dives because they likely correspond to coherent sub-conversations rather than arbitrary partitions: "
        + format_cluster_refs(stable, include_persistence=True)
        + ". In a pharmaceutical setting, these are the clusters most suitable for assigning to named owners because the chance of topic drift inside the packet is comparatively low. A concrete next step would be to split the first-pass review into separate briefs around "
        + " and ".join(interface_from_theme(str(row.theme)) for row in stable.itertuples())
        + ", instead of forcing one blended summary across the whole corpus.",
        "A second use is portfolio framing. The broadest clusters tell us which conversations are currently absorbing the largest share of the corpus and therefore may deserve separate workstreams or explicit review chapters: "
        + format_cluster_refs(broad, include_size=True)
        + ". When a single tutorial topic is dominated by one or two broad neighborhoods, that is usually a signal that any downstream summary should allocate dedicated space to those conversations rather than bury them under a generic disease-area overview. In practice, this means the review deck or scouting memo should probably reserve stand-alone sections for "
        + " and ".join(interface_from_theme(str(row.theme)) for row in broad.itertuples())
        + ".",
    ]

    if not bridge.empty:
        paragraphs.append(
            "A third use is cross-functional hypothesis generation. The most substantial bridge-like clusters are "
            + format_cluster_refs(bridge, include_size=True)
            + ". These are especially valuable for decision-making because they point to interface questions rather than siloed themes. In this run, the map suggests explicit follow-up around "
            + "; ".join(
                f"the interface between {interface_from_theme(str(row.theme))}"
                for row in bridge.itertuples()
            )
            + ". Those are the clusters most likely to generate cross-functional hypotheses, handoff questions, or combined search expansions."
        )

    if not review.empty:
        paragraphs.append(
            "Review-heavy hubs deserve a different treatment from mechanistic clusters. In this run, the main review-centered neighborhoods are "
            + format_cluster_refs(review)
            + ". These clusters are useful as orientation layers or onboarding packets, but they should not automatically be treated as evidence of a single mechanistic theme. A practical workflow is to use them first to frame the field, then route primary evidence extraction into denser neighborhoods such as "
            + " and ".join(interface_from_theme(str(row.theme)) for row in stable.itertuples())
            + "."
        )

    paragraphs.append(
        "A final use is opportunity finding. The least stable clusters are often where bridge papers, transitional themes, or representation-sensitive subtopics live. Those are the places most worth manual inspection if the goal is to identify white-space questions, cross-functional hypotheses, or emerging combinations: "
        + format_cluster_refs(weak, include_persistence=True)
        + ". The right reading is not that these clusters are unimportant, but that they are decision-sensitive: before acting on them, a team would usually want to inspect representative papers, rerun adjacent searches, or validate whether they reflect a real emerging topic rather than a boundary artifact. As a concrete policy, these clusters fit better into a watchlist or follow-up queue than into the backbone claims of a strategy document."
    )

    return paragraphs


def renumber_clusters(labels: np.ndarray) -> tuple[np.ndarray, dict[int, int]]:
    original_labels = sorted(label for label in set(labels.tolist()) if label != -1)
    mapping = {label: index + 1 for index, label in enumerate(original_labels)}
    renumbered = np.array([mapping.get(label, -1) for label in labels], dtype=int)
    return renumbered, mapping


def top_loading_rows(components: np.ndarray, vocabulary: list[str], explained_ratios: np.ndarray, n_components: int = 4) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    n = min(n_components, components.shape[0])
    for component_index in range(n):
        weights = components[component_index]
        positive_index = np.argsort(weights)[::-1][:5]
        negative_index = np.argsort(weights)[:5]
        for rank, vocab_index in enumerate(positive_index, start=1):
            rows.append(
                {
                    "component": f"PC{component_index + 1}",
                    "explained_variance_ratio": float(explained_ratios[component_index]),
                    "direction": "positive",
                    "rank": rank,
                    "term": vocabulary[vocab_index],
                    "loading": float(weights[vocab_index]),
                }
            )
        for rank, vocab_index in enumerate(negative_index, start=1):
            rows.append(
                {
                    "component": f"PC{component_index + 1}",
                    "explained_variance_ratio": float(explained_ratios[component_index]),
                    "direction": "negative",
                    "rank": rank,
                    "term": vocabulary[vocab_index],
                    "loading": float(weights[vocab_index]),
                }
            )
    return pd.DataFrame(rows)


def cluster_profiles(labels: np.ndarray, cluster_coords: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    component_count = min(4, cluster_coords.shape[1])
    for cluster_id in sorted(set(labels)):
        member_index = np.where(labels == cluster_id)[0]
        centroid = cluster_coords[member_index, :component_count].mean(axis=0)
        row: dict[str, object] = {"cluster_id": int(cluster_id)}
        for component_index in range(component_count):
            row[f"mean_pc{component_index + 1}"] = float(centroid[component_index])
        rows.append(row)
    return pd.DataFrame(rows)


def component_contrasts(profile_table: pd.DataFrame, explained_ratios: np.ndarray) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    component_columns = [column for column in profile_table.columns if column.startswith("mean_pc")]
    for idx, column in enumerate(component_columns):
        ordered = profile_table.sort_values(column)
        low = ordered.iloc[0]
        high = ordered.iloc[-1]
        rows.append(
            {
                "component": f"PC{idx + 1}",
                "explained_variance_ratio": float(explained_ratios[idx]),
                "low_cluster": int(low["cluster_id"]),
                "low_value": float(low[column]),
                "high_cluster": int(high["cluster_id"]),
                "high_value": float(high[column]),
                "gap": float(high[column] - low[column]),
            }
        )
    return pd.DataFrame(rows)


def render_case_html(study: StudySpec, cluster_summary: pd.DataFrame, contrast_table: pd.DataFrame, path: Path) -> None:
    cluster_rows = "".join(
        f"<tr><td>{'Noise' if int(row.cluster_id) == -1 else int(row.cluster_id)}</td><td>{row.theme}</td><td>{int(row.size)}</td><td>{row.mean_probability:.3f}</td><td>{row.persistence_display}</td></tr>"
        for row in cluster_summary.itertuples()
    )
    contrast_rows = "".join(
        f"<tr><td>{row.component}</td><td>{row.explained_variance_ratio * 100:.1f}%</td><td>{int(row.low_cluster)}</td><td>{row.low_value:.3f}</td><td>{int(row.high_cluster)}</td><td>{row.high_value:.3f}</td><td>{row.gap:.3f}</td></tr>"
        for row in contrast_table.itertuples()
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{study.title}</title>
<style>body{{margin:0;background:#f6f2ea;color:#172029;font-family:Georgia,serif}}main{{max-width:1120px;margin:0 auto;padding:32px 20px 56px}}.shell{{background:#fff;border:1px solid #d8ddd8;border-radius:18px;padding:24px}}iframe{{width:100%;height:760px;border:1px solid #d7dcd7;border-radius:14px}}table{{width:100%;border-collapse:collapse;margin-top:18px}}th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid #e5e7e3;vertical-align:top}}</style></head>
<body><main><div class="shell"><h1>{study.title}</h1><p>Interactive report preview generated from the bundled HDBSCAN tutorial corpus.</p><iframe src="map_interactive.html" title="{study.title} interactive map"></iframe><h2>Cluster summary</h2><table><thead><tr><th>Cluster</th><th>Theme</th><th>Size</th><th>Mean probability</th><th>Persistence</th></tr></thead><tbody>{cluster_rows}</tbody></table><h2>Component contrast snapshot</h2><table><thead><tr><th>Component</th><th>Explained variance</th><th>Low cluster</th><th>Low value</th><th>High cluster</th><th>High value</th><th>Gap</th></tr></thead><tbody>{contrast_rows}</tbody></table></div></main></body></html>"""
    path.write_text(html_doc, encoding="utf-8")


def article_paragraphs(paragraphs: list[str]) -> str:
    return "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)


def sample_rows(table: pd.DataFrame) -> str:
    chosen = table.iloc[[0, len(table) // 3, (2 * len(table)) // 3, len(table) - 1]]
    return "".join(
        f"<tr><td>{row.record_id}</td><td>{row.title}</td><td>{int(row.year)}</td><td>{row.record_type}</td></tr>"
        for row in chosen.itertuples()
    )


def build_result_discussion(
    labels_table: pd.DataFrame,
    cluster_summary: pd.DataFrame,
    contrast_table: pd.DataFrame,
    loading_table: pd.DataFrame,
) -> list[str]:
    non_noise = cluster_summary.loc[cluster_summary["cluster_id"] != -1].copy()
    if non_noise.empty:
        return [
            "This run was dominated by noise points, so the main interpretation is that the current corpus does not form stable high-density neighborhoods under the present preprocessing and HDBSCAN settings."
        ]

    top_clusters = non_noise.sort_values("size", ascending=False).head(3).reset_index(drop=True)
    largest = top_clusters.iloc[0]
    first_contrast = contrast_table.iloc[0]
    second_contrast = contrast_table.iloc[1] if len(contrast_table) > 1 else contrast_table.iloc[0]

    pos_pc1 = loading_table.loc[(loading_table["component"] == "PC1") & (loading_table["direction"] == "positive"), "term"].head(3).tolist()
    neg_pc1 = loading_table.loc[(loading_table["component"] == "PC1") & (loading_table["direction"] == "negative"), "term"].head(3).tolist()
    pos_pc2 = loading_table.loc[(loading_table["component"] == "PC2") & (loading_table["direction"] == "positive"), "term"].head(3).tolist()
    neg_pc2 = loading_table.loc[(loading_table["component"] == "PC2") & (loading_table["direction"] == "negative"), "term"].head(3).tolist()

    noise_count = int((labels_table["cluster"] == -1).sum())
    if len(top_clusters) > 1:
        next_clusters_text = ", ".join(
            f"Cluster {int(row.cluster_id)} ({row.theme}, {int(row.size)} records)"
            for row in top_clusters.iloc[1:].itertuples()
        )
        second_paragraph = (
            f"The next-largest groups are {next_clusters_text}. Looking at these sizes together is more informative than simply counting clusters, because it distinguishes between dominant neighborhoods and smaller specialist pockets. "
            f"The noise count is {noise_count}, which indicates how many records HDBSCAN judged not to belong confidently to any dense region."
        )
    else:
        second_paragraph = (
            f"The noise count is {noise_count}, which indicates how many records HDBSCAN judged not to belong confidently to any dense region."
        )
    paragraphs = [
        f"The largest density-defined neighborhood is Cluster {int(largest['cluster_id'])} ({largest['theme']}), with {int(largest['size'])} records. That matters because it suggests the corpus is not evenly structured: one conversation occupies a much denser or broader region of the analysis space than the others. In practical review work, that usually means one subtopic is acting as the dominant organizational center of the literature.",
        second_paragraph,
        f"In principal-component terms, the strongest first-axis contrast is between Cluster {int(first_contrast['low_cluster'])} and Cluster {int(first_contrast['high_cluster'])}, with a gap of {first_contrast['gap']:.3f} along PC1. The second-axis contrast is between Cluster {int(second_contrast['low_cluster'])} and Cluster {int(second_contrast['high_cluster'])}, with a gap of {second_contrast['gap']:.3f} along PC2. This is the concrete reason some neighborhoods look far apart in the map while others sit closer together: the separation is being driven by different components, not by one universal distance pattern.",
        f"The loading table helps interpret those axes. PC1 is pulled in its positive direction by terms such as {', '.join(pos_pc1) if pos_pc1 else 'n/a'} and in its negative direction by {', '.join(neg_pc1) if neg_pc1 else 'n/a'}. PC2 is pulled positively by {', '.join(pos_pc2) if pos_pc2 else 'n/a'} and negatively by {', '.join(neg_pc2) if neg_pc2 else 'n/a'}. That lets us move from a visual statement such as 'these clusters are apart' to a linguistic statement about what kinds of paper language are separating them.",
    ]
    return [paragraph for paragraph in paragraphs if paragraph.strip()]


def build_interpretation_discussion(
    cluster_summary: pd.DataFrame,
    contrast_table: pd.DataFrame,
    loading_table: pd.DataFrame,
) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "Because the output is dominated by noise, the most defensible interpretation is that this corpus does not support stable dense neighborhoods under the current representation and clustering settings."
        ]

    persistent = non_noise.sort_values(["persistence", "size"], ascending=[False, False]).head(2).reset_index(drop=True)
    broad = non_noise.sort_values(["size", "mean_probability"], ascending=[False, False]).head(2).reset_index(drop=True)
    weakest = non_noise.sort_values(["persistence", "mean_probability"], ascending=[True, True]).head(2).reset_index(drop=True)

    pc1_pos = loading_table.loc[(loading_table["component"] == "PC1") & (loading_table["direction"] == "positive"), "term"].head(3).tolist()
    pc1_neg = loading_table.loc[(loading_table["component"] == "PC1") & (loading_table["direction"] == "negative"), "term"].head(3).tolist()
    pc2_pos = loading_table.loc[(loading_table["component"] == "PC2") & (loading_table["direction"] == "positive"), "term"].head(3).tolist()
    pc2_neg = loading_table.loc[(loading_table["component"] == "PC2") & (loading_table["direction"] == "negative"), "term"].head(3).tolist()

    contrast1 = contrast_table.iloc[0]
    contrast2 = contrast_table.iloc[1] if len(contrast_table) > 1 else contrast_table.iloc[0]

    paragraphs = [
        f"The most stable neighborhoods in this run are "
        + ", ".join(
            f"Cluster {int(row.cluster_id)} ({row.theme}, persistence {row.persistence_display})"
            for row in persistent.itertuples()
        )
        + ". That matters because persistence is telling us these are not just visually isolated groups; they are comparatively robust density structures in the HDBSCAN hierarchy.",
        f"By contrast, the broadest neighborhoods are "
        + ", ".join(
            f"Cluster {int(row.cluster_id)} ({row.theme}, {int(row.size)} records)"
            for row in broad.itertuples()
        )
        + ". When a cluster is broad but only moderately persistent, it often behaves like a review-like or bridge-heavy basin rather than a sharply bounded mechanistic niche.",
        f"The least stable end of the solution is represented by "
        + ", ".join(
            f"Cluster {int(row.cluster_id)} ({row.theme}, persistence {row.persistence_display})"
            for row in weakest.itertuples()
        )
        + ". These are the places where the reader should be most cautious: they may still be meaningful, but they are more likely to reflect overlap zones or representation-sensitive splits.",
        f"Component interpretation sharpens that picture. PC1 separates Cluster {int(contrast1['low_cluster'])} from Cluster {int(contrast1['high_cluster'])}, and that axis is being pulled toward {', '.join(pc1_pos) if pc1_pos else 'n/a'} on one side and {', '.join(pc1_neg) if pc1_neg else 'n/a'} on the other. PC2 separates Cluster {int(contrast2['low_cluster'])} from Cluster {int(contrast2['high_cluster'])} and is pulled toward {', '.join(pc2_pos) if pc2_pos else 'n/a'} versus {', '.join(pc2_neg) if pc2_neg else 'n/a'}. In practical terms, these are the language patterns that explain why specific clusters sit in different parts of the map.",
    ]
    return paragraphs


def build_deep_dive_discussion(
    cluster_summary: pd.DataFrame,
    contrast_table: pd.DataFrame,
    loading_table: pd.DataFrame,
) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "Because there are no reliable non-noise clusters, a deeper read would first need a better representation or a narrower corpus before discussing substructure."
        ]

    broad = top_named_rows(non_noise, ["size", "mean_probability"], [False, False], limit=3)
    stable = top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=3)
    weak = top_named_rows(non_noise, ["persistence", "mean_probability"], [True, True], limit=2)
    bridge = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )

    paragraphs = [
        "A closer reading of the cluster table shows that not all themes are playing the same role in the landscape. "
        + "The broad clusters, "
        + format_cluster_refs(broad, include_size=True)
        + ", behave like the field's main basins. These are the conversations large enough to organize reading behavior by themselves, and they are often the ones that dominate strategy decks or internal onboarding because they collect both primary papers and broader synthesis language.",
        "The stable clusters, "
        + format_cluster_refs(stable, include_persistence=True)
        + ", tell a different story. Their value is not only size but coherence. If a team wanted to extract representative papers for subject-matter review, these are better starting points than the largest clusters because the likelihood of mixing incompatible sub-questions is lower.",
    ]

    if not bridge.empty:
        paragraphs.append(
            "The bridge clusters deserve special attention because they say something about where the field stops behaving like a set of isolated silos. "
            + format_cluster_refs(bridge, include_size=True)
            + " suggest that the literature is repeatedly linking "
            + " and ".join(interface_from_theme(str(row.theme)) for row in bridge.itertuples())
            + ". In practical terms, that is where a literature map becomes more than a taxonomy: it starts to highlight the junctions where program strategy, translational design, and modality questions may need to be discussed together."
        )

    if not review.empty:
        paragraphs.append(
            "The review-centered neighborhoods, "
            + format_cluster_refs(review, include_size=True)
            + ", also change how the output should be read. They usually inflate the apparent breadth of the field, but they are still useful. They tell us which combinations of themes are already being narrated together in the secondary literature. That is informative for communication and orientation, even if those clusters are not the right place to anchor mechanistic conclusions."
        )

    if not contrast_table.empty:
        top_components = contrast_table.head(3)
        component_text = ", ".join(
            f"{row.component} (gap {row.gap:.3f} between Cluster {int(row.low_cluster)} and Cluster {int(row.high_cluster)})"
            for row in top_components.itertuples()
        )
        paragraphs.append(
            "The PCA contrast table adds another layer to the interpretation. The most informative separating axes are "
            + component_text
            + ". That means the visual story of the map is not driven by one generic 'distance' notion. Different clusters are being separated by different latent contrasts, which is exactly why the map should be interpreted together with the loading and cluster-profile tables rather than in isolation."
        )

    paragraphs.append(
        "Finally, the weak clusters, "
        + format_cluster_refs(weak, include_persistence=True)
        + ", are not merely disposable leftovers. They often mark the boundary where the corpus is still negotiating topic identity. In a real review workflow, these are the places where one would expect to find edge cases, emerging terminology, or papers that force a rethink of the search strategy."
    )
    return paragraphs


def build_decision_memo(
    cluster_summary: pd.DataFrame,
    labels_table: pd.DataFrame,
) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "Recommended action: narrow the corpus or change the representation before using this run for decisions, because the current landscape does not support stable theme-level prioritization."
        ]

    stable = top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=2)
    broad = top_named_rows(non_noise, ["size", "mean_probability"], [False, False], limit=2)
    bridge = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    weak = top_named_rows(non_noise, ["persistence", "mean_probability"], [True, True], limit=2)
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=1,
    )
    noise_count = int((labels_table["cluster"] == -1).sum())

    memo = [
        "If this were a real portfolio scan, the first recommendation would be to separate 'orientation' work from 'evidence extraction'. The orientation layer should start from "
        + (format_cluster_refs(review) if not review.empty else format_cluster_refs(broad.head(1)))
        + ", because those clusters are best suited to framing the field. The evidence-extraction layer should start from "
        + format_cluster_refs(stable, include_persistence=True)
        + ", because these clusters are better candidates for high-confidence thematic reading packets.",
        "The second recommendation would be to reserve dedicated analysis bandwidth for "
        + format_cluster_refs(broad, include_size=True)
        + ". These clusters are large enough that collapsing them into a generic summary would likely hide the main organizing logic of the corpus. In a discovery, translational, or strategy setting, these are the themes that most deserve stand-alone synthesis documents or named workstreams.",
    ]
    if not bridge.empty:
        memo.append(
            "The third recommendation would be to hold a cross-functional discussion around "
            + format_cluster_refs(bridge, include_size=True)
            + ". These are exactly the clusters that can generate productive questions such as whether a target-biology issue is really a chemistry issue, whether a safety signal is constraining development strategy, or whether a biomarker theme is drifting into a broader translational problem."
        )
    memo.append(
        "The final recommendation concerns uncertainty management. "
        + format_cluster_refs(weak, include_persistence=True)
        + f" and the {noise_count} noise points should not be ignored, but they also should not anchor headline claims. They fit better into a watchlist, an emerging-topic appendix, or a second-pass search expansion than into the core claims of a review memo."
    )
    return memo


def build_next_actions(
    cluster_summary: pd.DataFrame,
    labels_table: pd.DataFrame,
) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    if non_noise.empty:
        return [
            "1. Narrow the corpus definition or adjust the embedding and clustering settings before treating this map as decision support.",
            "2. Re-run the search with a clearer inclusion boundary so that the next pass tests whether dense neighborhoods emerge under a better-defined corpus.",
        ]

    stable = top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=2)
    bridge = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    weak = top_named_rows(non_noise, ["persistence", "mean_probability"], [True, True], limit=2)
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=1,
    )

    actions: list[str] = []
    if not stable.empty:
        actions.append(
            "1. Build first-pass reading packets around "
            + format_cluster_refs(stable)
            + ". These are the safest clusters for detailed reading because coherence and assignment confidence are both relatively high."
        )
    if not review.empty:
        actions.append(
            "2. Use "
            + format_cluster_refs(review)
            + " as the orientation layer. Start there for framing, but shift evidence extraction into the denser mechanistic clusters so review language does not dominate the final interpretation."
        )
    if not bridge.empty:
        actions.append(
            "3. Hold a cross-functional review around "
            + format_cluster_refs(bridge)
            + ". These clusters are the best places to test whether separate workstreams should actually be merged into a shared translational question."
        )
    actions.append(
        "4. Put "
        + format_cluster_refs(weak)
        + " on a watchlist. Treat them as candidates for follow-up searches, representative-paper inspection, or a separate appendix rather than as the backbone of a strategy narrative."
    )
    return actions


def build_reading_table(cluster_summary: pd.DataFrame, labels_table: pd.DataFrame) -> str:
    non_noise = named_cluster_rows(cluster_summary)
    reading_clusters = top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=3)
    rows: list[str] = []
    for row in reading_clusters.itertuples():
        subset = labels_table.loc[labels_table["cluster"] == int(row.cluster_id)].sort_values("probability", ascending=False).head(3)
        examples = "<br>".join(subset["title"].tolist())
        rows.append(
            f"<tr><td>Cluster {int(row.cluster_id)}</td><td>{row.theme}</td><td>{row.persistence_display}</td><td>{examples}</td></tr>"
        )
    return "".join(rows)


def owner_role_for_theme(theme: str) -> str:
    lowered = theme.lower()
    if theme.startswith("Bridge: "):
        return "Cross-functional working pair"
    if theme.startswith("Review hub: "):
        return "Landscape / competitive intelligence lead"
    if "safety" in lowered or "toxicity" in lowered:
        return "Clinical pharmacology / safety lead"
    if "biomarker" in lowered or "monitoring" in lowered or "mrd" in lowered or "ctdna" in lowered:
        return "Translational biomarker lead"
    if "target" in lowered or "ligase" in lowered or "resistance" in lowered:
        return "Biology lead"
    if "linker" in lowered or "payload" in lowered or "degrader" in lowered or "ternary" in lowered:
        return "Medicinal chemistry lead"
    if "pk" in lowered or "translation" in lowered or "dose" in lowered:
        return "DMPK / translational lead"
    return "Portfolio strategy lead"


def build_owner_assignment_table(cluster_summary: pd.DataFrame) -> str:
    non_noise = named_cluster_rows(cluster_summary)
    selected = pd.concat(
        [
            top_named_rows(non_noise, ["persistence", "size"], [False, False], limit=2),
            top_named_rows(non_noise, ["size", "mean_probability"], [False, False], limit=2),
            top_named_rows(
                non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
                ["size", "persistence"],
                [False, False],
                limit=1,
            ),
        ],
        ignore_index=True,
    ).drop_duplicates(subset=["cluster_id"]).reset_index(drop=True)
    rows: list[str] = []
    for row in selected.itertuples():
        role = owner_role_for_theme(str(row.theme))
        rationale = (
            f"Stable enough to anchor close reading"
            if float(row.persistence) >= 0.2
            else "Broad or cross-cutting enough to require coordinated review"
        )
        rows.append(
            f"<tr><td>Cluster {int(row.cluster_id)}</td><td>{row.theme}</td><td>{role}</td><td>{rationale}</td></tr>"
        )
    return "".join(rows)


def build_search_expansion_table(cluster_summary: pd.DataFrame) -> str:
    non_noise = named_cluster_rows(cluster_summary)
    bridge = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "bridge"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    weak = top_named_rows(non_noise, ["persistence", "mean_probability"], [True, True], limit=2)
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=1,
    )
    rows: list[str] = []
    for row in bridge.itertuples():
        interface = str(row.theme).removeprefix("Bridge: ").replace(" x ", " + ")
        rows.append(
            f"<tr><td>Bridge follow-up</td><td>Cluster {int(row.cluster_id)}</td><td>{interface}</td><td>Expand the query with terms that explicitly combine {interface.lower()} to test whether the bridge is a durable subfield or an artifact of mixed papers.</td></tr>"
        )
    for row in weak.itertuples():
        rows.append(
            f"<tr><td>Boundary validation</td><td>Cluster {int(row.cluster_id)}</td><td>{row.theme}</td><td>Run a narrower adjacent search around this theme to see whether the weak cluster tightens into a coherent neighborhood under a more specific corpus definition.</td></tr>"
        )
    for row in review.itertuples():
        rows.append(
            f"<tr><td>Secondary-literature framing</td><td>Cluster {int(row.cluster_id)}</td><td>{row.theme}</td><td>Use the review-hub language to discover adjacent umbrella reviews, then separate those from primary evidence so the next pass distinguishes orientation from mechanism.</td></tr>"
        )
    return "".join(rows)


def build_gap_audit(cluster_summary: pd.DataFrame, labels_table: pd.DataFrame, pca_cluster_components: pd.DataFrame) -> list[str]:
    non_noise = named_cluster_rows(cluster_summary)
    noise_count = int((labels_table["cluster"] == -1).sum())
    first_pc = float(pca_cluster_components.iloc[0]["explained_variance_ratio"]) if not pca_cluster_components.empty else 0.0
    weak = top_named_rows(non_noise, ["persistence", "mean_probability"], [True, True], limit=2)
    review = top_named_rows(
        non_noise.loc[non_noise["theme"].map(theme_family) == "review"],
        ["size", "persistence"],
        [False, False],
        limit=2,
    )
    gaps = [
        f"The article is still limited by projection. PC1 explains only {first_pc * 100:.2f}% of variance, so the 2D map is useful but necessarily incomplete. That is why the cluster tables and PCA contrasts are essential rather than optional appendix material.",
        f"The run also leaves ambiguity in the weakest clusters, especially {format_cluster_refs(weak, include_persistence=True)}. Those clusters deserve follow-up rather than overconfident interpretation.",
        f"Noise is low at {noise_count} records, which is good for coverage but also means the representation is pulling most documents into some neighborhood. In review practice, that is a reason to sanity-check whether broad clusters are absorbing borderline material too aggressively.",
    ]
    if not review.empty:
        gaps.append(
            "Review-heavy neighborhoods remain a source of interpretive inflation. "
            + format_cluster_refs(review, include_size=True)
            + " are useful for orientation, but they can make the field look more thematically settled than the primary literature actually is."
        )
    return gaps


def write_article(
    study: StudySpec,
    records: pd.DataFrame,
    labels_table: pd.DataFrame,
    cluster_summary: pd.DataFrame,
    pca_cluster_components: pd.DataFrame,
    pca_plot_components: pd.DataFrame,
    loading_table: pd.DataFrame,
    profile_table: pd.DataFrame,
    contrast_table: pd.DataFrame,
) -> None:
    article_path = TUTORIAL_DIR / f"{study.slug}.html"
    markdown_path = TUTORIAL_DIR / f"{study.slug}.md"
    cluster_rows = "".join(
        f"<tr><td>{'Noise' if int(row.cluster_id) == -1 else int(row.cluster_id)}</td><td>{row.theme}</td><td>{int(row.size)}</td><td>{row.mean_probability:.3f}</td><td>{row.persistence_display}</td></tr>"
        for row in cluster_summary.itertuples()
    )
    loading_rows = "".join(
        f"<tr><td>{row.component}</td><td>{row.direction}</td><td>{row.term}</td><td>{row.loading:.4f}</td></tr>"
        for row in loading_table.head(24).itertuples()
    )
    profile_rows = "".join(
        f"<tr><td>{'Noise' if int(row.cluster_id) == -1 else int(row.cluster_id)}</td><td>{row.mean_pc1:.3f}</td><td>{row.mean_pc2:.3f}</td><td>{row.mean_pc3:.3f}</td><td>{row.mean_pc4:.3f}</td></tr>"
        for row in profile_table.itertuples()
    )
    contrast_rows = "".join(
        f"<tr><td>{row.component}</td><td>{row.explained_variance_ratio * 100:.1f}%</td><td>{int(row.low_cluster)}</td><td>{row.low_value:.3f}</td><td>{int(row.high_cluster)}</td><td>{row.high_value:.3f}</td><td>{row.gap:.3f}</td></tr>"
        for row in contrast_table.itertuples()
    )
    pca_cluster_rows = "".join(
        f"<tr><td>{row.component}</td><td>{row.explained_variance_ratio * 100:.2f}%</td></tr>"
        for row in pca_cluster_components.head(8).itertuples()
    )
    pca_plot_rows = "".join(
        f"<tr><td>{row.component}</td><td>{row.explained_variance_ratio * 100:.2f}%</td></tr>"
        for row in pca_plot_components.itertuples()
    )
    highlight_items = "".join(f"<li>{item}</li>" for item in build_headline_findings(cluster_summary, labels_table, contrast_table))
    next_action_items = "".join(f"<li>{item}</li>" for item in build_next_actions(cluster_summary, labels_table))
    reading_rows = build_reading_table(cluster_summary, labels_table)
    owner_rows = build_owner_assignment_table(cluster_summary)
    expansion_rows = build_search_expansion_table(cluster_summary)

    n_clusters = int((cluster_summary["cluster_id"] != -1).sum())
    noise_count = int((labels_table["cluster"] == -1).sum())
    largest_cluster = cluster_summary.loc[cluster_summary["cluster_id"] != -1].sort_values("size", ascending=False).head(1)
    if not largest_cluster.empty:
        largest_cluster_id = int(largest_cluster.iloc[0]["cluster_id"])
        largest_cluster_name = largest_cluster.iloc[0]["theme"]
        largest_cluster_size = int(largest_cluster.iloc[0]["size"])
    else:
        largest_cluster_id = -1
        largest_cluster_name = "noise-dominated output"
        largest_cluster_size = 0

    results_text = [
        f"The HDBSCAN run produced {n_clusters} non-noise clusters and {noise_count} noise points. This is already a meaningful difference from the older tutorial version, which forced every topic into exactly four groups. Here the cluster count is an empirical result of local density structure in the reduced analysis space.",
        f"The largest discovered neighborhood is Cluster {largest_cluster_id} ({largest_cluster_name}) with {largest_cluster_size} records. Large clusters in this setting often correspond to broad review-like or high-density translational neighborhoods, whereas smaller clusters tend to capture more technically specific pockets of the corpus.",
        "The key practical consequence is that the map is now allowed to admit ambiguity. Borderline or weakly connected records can remain as noise, and neighborhoods do not have to occupy equal volume. That is much closer to what one expects from a real literature landscape than a fixed-k partition.",
    ]
    results_text.extend(build_result_discussion(labels_table, cluster_summary, contrast_table, loading_table))

    interpretation_text = [
        *study.interpretation,
        "This also explains why the number of visual islands in the map does not have to match the number of HDBSCAN clusters. Clustering is performed in a higher-dimensional PCA space, while the map is only a two-dimensional display projection. Distinctions that are clear in PC3 or PC4 may partially disappear in the rendered map, and one broad-looking area may still contain multiple density-defined structures.",
        "The component-level tables are included precisely to make that gap interpretable. The cluster profile table shows where each cluster centroid sits in principal-component space, while the component contrast table shows which pairs of clusters are most separated along each axis. That lets the article move from descriptive plotting to an explicit explanation of why the structure looks the way it does.",
    ]
    interpretation_text.extend(build_interpretation_discussion(cluster_summary, contrast_table, loading_table))
    deep_dive_text = build_deep_dive_discussion(cluster_summary, contrast_table, loading_table)
    perspective_text = build_perspective_discussion(cluster_summary)
    decision_memo_text = build_decision_memo(cluster_summary, labels_table)
    gap_audit_text = build_gap_audit(cluster_summary, labels_table, pca_cluster_components)

    html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{study.title} | litmap</title>
<style>:root{{--bg:#f4efe6;--panel:rgba(255,251,245,0.9);--ink:#172029;--accent:#0f6c5c;--line:rgba(23,32,41,0.12);--muted:#58636d;--hero:#0f6c5c;--hero-ink:#f5f7f2;}}body{{margin:0;font-family:"Palatino Linotype",Georgia,serif;color:var(--ink);background:linear-gradient(180deg,#efe7d9 0%,#f5f7f2 100%);}}main{{max-width:1160px;margin:0 auto;padding:42px 24px 72px;}}.hero,.panel{{background:var(--panel);border:1px solid var(--line);border-radius:22px;box-shadow:0 18px 48px rgba(23,32,41,0.08);}}.hero{{padding:36px;margin-bottom:22px;background:linear-gradient(140deg,#17382f 0%,#0f6c5c 56%,#1f8d78 100%);color:var(--hero-ink);}}.hero a{{color:#fff;}}.panel{{padding:28px;margin-bottom:22px;}}h1,h2,h3{{margin-top:0;}}p,li{{line-height:1.9;font-size:1.03rem;}}a{{color:var(--accent);}}pre,code{{font-family:Consolas,"Courier New",monospace;}}pre{{overflow-x:auto;padding:16px;border-radius:14px;background:#1c252d;color:#f9f5ee;}}table{{width:100%;border-collapse:collapse;}}th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid #e5e7e3;vertical-align:top;}}.muted{{color:var(--muted);}}.hero .muted{{color:rgba(245,247,242,0.76);}}.linkrow{{display:flex;flex-wrap:wrap;gap:14px;}}iframe{{width:100%;height:760px;border:1px solid #d7dcd7;border-radius:16px;background:#fff;}}.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:22px;}}.highlight-box{{background:#f7fbf8;border:1px solid rgba(15,108,92,0.18);border-radius:18px;padding:22px;}}.section-kicker{{font-size:0.86rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;}}.hero .section-kicker{{color:rgba(245,247,242,0.8);}}ul.tight{{margin:0;padding-left:22px;}}@media (max-width: 960px){{.twocol{{grid-template-columns:1fr;}}}}</style></head>
<body><main><section class="hero"><p class="muted">Tutorial article</p><h1>{study.title}</h1><p>This article documents a generated tutorial run from the bundled corpus in <code>docs/tutorial-data/{study.slug}.csv</code>. The analysis path is <code>TF-IDF -&gt; L2 normalize -&gt; PCA(cluster space) -&gt; HDBSCAN -&gt; PCA(plot space) -&gt; Plotly</code>.</p><div class="linkrow"><a href="index.html">All tutorials</a><a href="../case-studies/{study.slug}/map_interactive.html">Open interactive map</a><a href="{study.slug}.md">Open Markdown source</a></div></section>
<section class="panel"><h2>Background</h2>{article_paragraphs(study.background)}</section>
<section class="panel"><h2>Purpose</h2>{article_paragraphs(study.purpose)}</section>
<section class="panel"><p class="section-kicker">Executive summary</p><h2>Headline findings</h2><div class="highlight-box"><ul class="tight">{highlight_items}</ul></div></section>
<section class="panel"><h2>Data used</h2><p>Source file: <a href="../tutorial-data/{study.slug}.csv">{study.slug}.csv</a>. The bundled corpus contains {len(records)} records. The corpus is deterministic and generated for tutorial purposes, but it is built to contain core papers, crossover papers, and review-like records so that density structure is not artificially trivial.</p><table><thead><tr><th>Record</th><th>Title</th><th>Year</th><th>Type</th></tr></thead><tbody>{sample_rows(records)}</tbody></table><p>The main reason for explicitly listing sample rows is to make the tutorial article inspectable. A reader should be able to see what kinds of documents were analyzed, not just trust a figure after the fact.</p></section>
<section class="panel"><h2>Code used</h2><pre>embedding = build_tfidf_embeddings(texts)
normalized = l2_normalize(embedding.matrix)
cluster_space = run_pca(normalized, n_components=50)
cluster_result = run_hdbscan(cluster_space.coordinates, config)
plot_space = run_pca(normalized, n_components=2)
figure = build_plotly_map(result_table, title=study.title)</pre><p>The important design choice is that clustering and display are separated. HDBSCAN works in the higher-dimensional cluster space, while the map is rendered from a separate 2D PCA projection. That makes it possible to discuss why cluster count and visible map islands may diverge.</p></section>
<section class="panel"><h2>Results</h2><iframe src="../case-studies/{study.slug}/map_interactive.html" title="{study.title} interactive map"></iframe>{article_paragraphs(results_text)}<table><thead><tr><th>Cluster</th><th>Theme</th><th>Size</th><th>Mean probability</th><th>Persistence</th></tr></thead><tbody>{cluster_rows}</tbody></table></section>
<section class="panel"><h2>What to read first</h2><p>The table below is designed as a practical reading aid. It prioritizes the most stable clusters and surfaces a few representative papers from each one so that the article can lead directly into human review work.</p><table><thead><tr><th>Cluster</th><th>Theme</th><th>Persistence</th><th>Representative papers</th></tr></thead><tbody>{reading_rows}</tbody></table></section>
<section class="panel"><h2>PCA summary</h2><div class="twocol"><div><h3>Cluster-space PCA</h3><table><thead><tr><th>Component</th><th>Explained variance ratio</th></tr></thead><tbody>{pca_cluster_rows}</tbody></table></div><div><h3>Plot-space PCA</h3><table><thead><tr><th>Component</th><th>Explained variance ratio</th></tr></thead><tbody>{pca_plot_rows}</tbody></table></div></div><p>The cluster-space PCA is the one that matters for HDBSCAN because it defines the analysis geometry. The plot-space PCA is only used to place points on a readable map. Keeping those roles separate makes it much easier to explain why a 2D figure can never be a perfect picture of the clustering space.</p><h3>Cluster mean positions in principal-component space</h3><table><thead><tr><th>Cluster</th><th>Mean PC1</th><th>Mean PC2</th><th>Mean PC3</th><th>Mean PC4</th></tr></thead><tbody>{profile_rows}</tbody></table><h3>Component-level cluster separation</h3><table><thead><tr><th>Component</th><th>Explained variance</th><th>Low cluster</th><th>Low value</th><th>High cluster</th><th>High value</th><th>Gap</th></tr></thead><tbody>{contrast_rows}</tbody></table><h3>Top loading terms</h3><table><thead><tr><th>Component</th><th>Direction</th><th>Term</th><th>Loading</th></tr></thead><tbody>{loading_rows}</tbody></table></section>
<section class="panel"><h2>Interpretation and discussion</h2>{article_paragraphs(interpretation_text)}</section>
<section class="panel"><h2>Deeper read of the landscape</h2>{article_paragraphs(deep_dive_text)}</section>
<section class="panel"><h2>What is still missing</h2>{article_paragraphs(gap_audit_text)}</section>
<section class="panel"><h2>Perspective for decision-making</h2>{article_paragraphs(perspective_text)}</section>
<section class="panel"><h2>Decision memo</h2>{article_paragraphs(decision_memo_text)}</section>
<section class="panel"><h2>Owner assignment</h2><p>This short table translates clusters into plausible review ownership so that the output can be used in a real review workflow rather than only as an analytical artifact.</p><table><thead><tr><th>Cluster</th><th>Theme</th><th>Suggested owner</th><th>Why this owner</th></tr></thead><tbody>{owner_rows}</tbody></table></section>
<section class="panel"><h2>Search expansion ideas</h2><p>These query ideas are meant to turn the map into a second-pass search plan. The point is not to search blindly, but to use cluster structure to decide where recall should be increased or sharpened.</p><table><thead><tr><th>Use case</th><th>Target cluster</th><th>Theme</th><th>Expansion idea</th></tr></thead><tbody>{expansion_rows}</tbody></table></section>
<section class="panel"><h2>Recommended next actions</h2><div class="highlight-box"><ul class="tight">{next_action_items}</ul></div></section>
<section class="panel"><h2>Generated artifacts</h2><ul><li><a href="../case-studies/{study.slug}/labels.csv">labels.csv</a></li><li><a href="../case-studies/{study.slug}/cluster_summary.csv">cluster_summary.csv</a></li><li><a href="../case-studies/{study.slug}/coords_2d.csv">coords_2d.csv</a></li><li><a href="../case-studies/{study.slug}/pca_cluster_components.csv">pca_cluster_components.csv</a></li><li><a href="../case-studies/{study.slug}/pca_plot_components.csv">pca_plot_components.csv</a></li><li><a href="../case-studies/{study.slug}/pca_loadings.csv">pca_loadings.csv</a></li><li><a href="../case-studies/{study.slug}/cluster_component_profile.csv">cluster_component_profile.csv</a></li><li><a href="../case-studies/{study.slug}/component_cluster_contrast.csv">component_cluster_contrast.csv</a></li><li><a href="../case-studies/{study.slug}/map_interactive.html">map_interactive.html</a></li><li><a href="../case-studies/{study.slug}/analysis_manifest.json">analysis_manifest.json</a></li></ul></section>
</main></body></html>"""
    article_path.write_text(html_doc, encoding="utf-8")

    markdown = f"""# Tutorial: {study.title}

This article documents a generated tutorial run from the bundled corpus in `docs/tutorial-data/{study.slug}.csv`. The analysis path is `TF-IDF -> L2 normalize -> PCA(cluster space) -> HDBSCAN -> PCA(plot space) -> Plotly`.

## Background

""" + "\n\n".join(study.background) + f"""

## Purpose

""" + "\n\n".join(study.purpose) + f"""

## Results

- Non-noise clusters discovered: {n_clusters}
- Noise points: {noise_count}
- Largest non-noise cluster: {largest_cluster_id} ({largest_cluster_name}), {largest_cluster_size} records

## Generated artifacts

- [labels.csv](../case-studies/{study.slug}/labels.csv)
- [cluster_summary.csv](../case-studies/{study.slug}/cluster_summary.csv)
- [coords_2d.csv](../case-studies/{study.slug}/coords_2d.csv)
- [pca_cluster_components.csv](../case-studies/{study.slug}/pca_cluster_components.csv)
- [pca_plot_components.csv](../case-studies/{study.slug}/pca_plot_components.csv)
- [pca_loadings.csv](../case-studies/{study.slug}/pca_loadings.csv)
- [cluster_component_profile.csv](../case-studies/{study.slug}/cluster_component_profile.csv)
- [component_cluster_contrast.csv](../case-studies/{study.slug}/component_cluster_contrast.csv)
- [map_interactive.html](../case-studies/{study.slug}/map_interactive.html)
"""
    markdown_path.write_text(markdown, encoding="utf-8")


def update_tutorial_index(studies: list[StudySpec]) -> None:
    cards = "\n".join(
        f'<article class="card"><p class="eyebrow">Case study</p><h2><a href="{study.slug}.html">{study.title}</a></h2><p>{study.purpose[0]}</p><p><a href="{study.slug}.html">Read the full article</a></p></article>'
        for study in studies
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>litmap tutorials</title>
<style>:root{{--bg:#f4efe6;--panel:rgba(255,251,245,0.88);--ink:#172029;--accent:#0f6c5c;--line:rgba(23,32,41,0.12);--muted:#58636d;}}body{{margin:0;font-family:"Palatino Linotype",Georgia,serif;color:var(--ink);background:radial-gradient(circle at top left,rgba(15,108,92,0.16),transparent 24%),linear-gradient(160deg,#ece6d9 0%,var(--bg) 48%,#edf3ef 100%);}}main{{max-width:1100px;margin:0 auto;padding:48px 24px 80px;}}.hero,.card{{background:var(--panel);border:1px solid var(--line);border-radius:22px;box-shadow:0 18px 56px rgba(23,32,41,0.08);}}.hero{{padding:40px;margin-bottom:26px;}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;}}.card{{padding:22px;}}h1,h2{{margin-top:0;}}p{{line-height:1.7;}}a{{color:var(--accent);}}.muted{{color:var(--muted);}}.eyebrow{{font-size:0.82rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;}}</style></head>
<body><main><section class="hero"><p class="muted">litmap / tutorials</p><h1>Case-study articles built around actual clustering results</h1><p>These tutorials are written as long-form analytical articles rather than short package demos. Each one now includes a headline summary, a concrete reading of the major clusters, a 'what to read first' section, a gap audit, owner assignment ideas, search expansion ideas, a decision memo, and explicit next actions that tie the map back to review, scouting, or portfolio work.</p><p><a href="../index.html">Back to docs home</a></p></section><section class="cards">{cards}</section></main></body></html>"""
    (TUTORIAL_DIR / "index.html").write_text(html_doc, encoding="utf-8")


def analyze_study(study: StudySpec) -> None:
    records = generate_records(study)
    records["text_for_embedding"] = records["title"] + " [SEP] " + records["abstract"]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_path = DATA_DIR / f"{study.slug}.csv"
    records.to_csv(data_path, index=False)

    embedding = build_tfidf_embeddings(records["text_for_embedding"].tolist(), min_df=2, ngram_range=(1, 2))
    normalized = l2_normalize(embedding.matrix)

    n_cluster_components = min(50, normalized.shape[0], normalized.shape[1])
    cluster_pca = run_pca(normalized, n_components=n_cluster_components)
    hdbscan_config = HDBSCANConfig(
        min_cluster_size="auto",
        min_cluster_size_floor=15,
        min_cluster_size_ratio=0.01,
        min_samples=None,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    cluster_result = run_hdbscan(cluster_pca.coordinates, hdbscan_config)
    plot_pca = run_pca(normalized, n_components=2)

    display_labels, cluster_mapping = renumber_clusters(cluster_result.labels)
    original_themes = infer_cluster_themes(cluster_result.labels, normalized, embedding.vocabulary)
    themes: dict[int, str] = {}
    for original_id, fallback_theme in original_themes.items():
        display_id = cluster_mapping[original_id]
        subset = records.loc[cluster_result.labels == original_id]
        themes[display_id] = article_theme_name(subset, fallback_theme)

    out_dir = CASE_DIR / study.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    labels_table = records.copy()
    labels_table["original_cluster_id"] = cluster_result.labels
    labels_table["cluster"] = display_labels
    labels_table["probability"] = cluster_result.probabilities
    labels_table["cluster_display"] = ["Noise" if label == -1 else f"Cluster {label}" for label in display_labels]
    labels_table["cluster_theme"] = [resolve_cluster_label(label, themes) for label in display_labels]
    labels_table["pc1_plot"] = plot_pca.coordinates[:, 0]
    labels_table["pc2_plot"] = plot_pca.coordinates[:, 1]
    labels_table["pc1_cluster"] = cluster_pca.coordinates[:, 0]
    labels_table["pc2_cluster"] = cluster_pca.coordinates[:, 1]
    labels_table["pc3_cluster"] = cluster_pca.coordinates[:, 2] if cluster_pca.coordinates.shape[1] > 2 else 0.0
    labels_table["pc4_cluster"] = cluster_pca.coordinates[:, 3] if cluster_pca.coordinates.shape[1] > 3 else 0.0
    labels_table.to_csv(out_dir / "labels.csv", index=False)
    labels_table.loc[:, ["record_id", "pc1_plot", "pc2_plot", "cluster"]].to_csv(out_dir / "coords_2d.csv", index=False)

    persistence_map = {cluster_mapping[cluster_id]: float(cluster_result.cluster_persistence[cluster_id]) for cluster_id in range(len(cluster_result.cluster_persistence))}
    summary_rows: list[dict[str, object]] = []
    for cluster_id in sorted(set(display_labels)):
        subset = labels_table.loc[labels_table["cluster"] == cluster_id]
        summary_rows.append(
            {
                "cluster_id": int(cluster_id),
                "theme": resolve_cluster_label(cluster_id, themes),
                "size": int(len(subset)),
                "mean_probability": float(subset["probability"].mean()),
                "persistence": None if cluster_id == -1 else persistence_map.get(cluster_id),
                "persistence_display": "n/a" if cluster_id == -1 else f"{persistence_map.get(cluster_id, float('nan')):.3f}",
                "representative_papers": representative_titles(labels_table, cluster_id),
            }
        )
    cluster_summary = pd.DataFrame(summary_rows).sort_values(["cluster_id"]).reset_index(drop=True)
    cluster_summary.to_csv(out_dir / "cluster_summary.csv", index=False)

    pca_cluster_components = pd.DataFrame(
        {
            "component": [f"PC{i + 1}" for i in range(len(cluster_pca.explained_variance_ratio))],
            "explained_variance_ratio": cluster_pca.explained_variance_ratio,
        }
    )
    pca_cluster_components.to_csv(out_dir / "pca_cluster_components.csv", index=False)
    pca_plot_components = pd.DataFrame(
        {
            "component": ["PC1", "PC2"],
            "explained_variance_ratio": plot_pca.explained_variance_ratio,
        }
    )
    pca_plot_components.to_csv(out_dir / "pca_plot_components.csv", index=False)

    loading_table = top_loading_rows(
        cluster_pca.model.components_,
        embedding.vocabulary,
        cluster_pca.explained_variance_ratio,
        n_components=min(4, cluster_pca.model.components_.shape[0]),
    )
    loading_table.to_csv(out_dir / "pca_loadings.csv", index=False)

    profile_table = cluster_profiles(display_labels, cluster_pca.coordinates)
    profile_table.to_csv(out_dir / "cluster_component_profile.csv", index=False)

    contrast_table = component_contrasts(profile_table, cluster_pca.explained_variance_ratio)
    contrast_table.to_csv(out_dir / "component_cluster_contrast.csv", index=False)

    figure = build_plotly_map(labels_table, title=study.title, opacity=0.64)
    write_plotly_html(figure, out_dir / "map_interactive.html")
    render_case_html(study, cluster_summary, contrast_table, out_dir / "map_static.html")

    manifest = {
        "slug": study.slug,
        "title": study.title,
        "record_count": int(len(records)),
        "analysis_backend": "tfidf_l2_pca_hdbscan_pca_plotly",
        "cluster_count_non_noise": int((cluster_summary["cluster_id"] != -1).sum()),
        "noise_count": int((labels_table["cluster"] == -1).sum()),
        "generated_from": str(data_path.relative_to(ROOT)),
    }
    (out_dir / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    write_article(
        study,
        records,
        labels_table,
        cluster_summary,
        pca_cluster_components,
        pca_plot_components,
        loading_table,
        profile_table,
        contrast_table,
    )


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CASE_DIR.mkdir(parents=True, exist_ok=True)
    TUTORIAL_DIR.mkdir(parents=True, exist_ok=True)
    for study in STUDIES:
        analyze_study(study)
    update_tutorial_index(STUDIES)
    print("Generated studies:", ", ".join(study.slug for study in STUDIES))


if __name__ == "__main__":
    main()
