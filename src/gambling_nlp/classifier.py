"""Weak supervision: lexicon hits as labels, char-ngram TF-IDF + logreg.

Purpose is lexicon expansion, not validation: the classifier learns from
lexicon-derived labels, so its scores are only as good as the seed. Its
useful output is the ranking of documents that contain *no* seed term but
look like the labelled class — candidates for human review.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline

from .lexicon import GAMBLING_CATEGORIES, all_terms
from .scoring import score_text


def weak_labels(texts: list[str], categories: tuple[str, ...] = GAMBLING_CATEGORIES) -> np.ndarray:
    """1 = document has a non-negated hit in any of ``categories``."""
    return np.array([
        1 if any(score_text(t).category_counts[c] > 0 for c in categories) else 0
        for t in texts
    ])


def build_model() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2, 4),
                                  min_df=2, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])


@dataclass
class WeakSupervisionReport:
    n_docs: int
    n_positive: int
    cv_auc: float | None
    novel_candidates: list[tuple[str, float]]
    note: str = ""


def train_and_report(texts: list[str],
                     categories: tuple[str, ...] = GAMBLING_CATEGORIES,
                     top_novel: int = 10, cv: int = 5,
                     min_positive: int = 30) -> tuple[Pipeline | None, WeakSupervisionReport]:
    """Fit on weak labels; return model plus CV AUC and lexicon-missed candidates.

    If the labelled class is too sparse to cross-validate, returns no model
    and says so: a sparse seed tier cannot bootstrap a classifier, which is
    itself a reportable property of the lexicon/corpus pair.
    """
    y = weak_labels(texts, categories)
    n_pos = int(y.sum())
    if n_pos < min_positive:
        return None, WeakSupervisionReport(
            n_docs=len(texts), n_positive=n_pos, cv_auc=None, novel_candidates=[],
            note=f"only {n_pos} positive documents for {categories}; "
                 f"too sparse to bootstrap (min {min_positive})",
        )

    model = build_model()
    proba = cross_val_predict(model, texts, y, cv=cv, method="predict_proba")[:, 1]
    auc = float(roc_auc_score(y, proba))

    model.fit(texts, y)
    scores = model.predict_proba(texts)[:, 1]
    seed = set(all_terms())
    novel = [
        (t, float(s)) for t, s, label in zip(texts, scores, y)
        if label == 0 and not any(term in t for term in seed)
    ]
    novel.sort(key=lambda x: -x[1])
    return model, WeakSupervisionReport(
        n_docs=len(texts), n_positive=n_pos, cv_auc=auc,
        novel_candidates=novel[:top_novel],
    )
