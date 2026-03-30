from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass(slots=True)
class TfidfEmbeddingResult:
    matrix: np.ndarray
    vocabulary: list[str]
    vectorizer: TfidfVectorizer


def build_tfidf_embeddings(texts: list[str], min_df: int = 2, ngram_range: tuple[int, int] = (1, 2)) -> TfidfEmbeddingResult:
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        min_df=min_df,
        ngram_range=ngram_range,
    )
    matrix = vectorizer.fit_transform(texts).toarray()
    vocabulary = vectorizer.get_feature_names_out().tolist()
    return TfidfEmbeddingResult(matrix=matrix, vocabulary=vocabulary, vectorizer=vectorizer)
