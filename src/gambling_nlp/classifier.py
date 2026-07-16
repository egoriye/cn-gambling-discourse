"""Weak supervision: lexicon hits as labels, char-ngram TF-IDF + logreg.

Goal: generalise beyond the seed lexicon and rank lexicon-missed
candidates for review (standard dictionary-bootstrap recipe).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline

from .scoring import score_text


def weak_labels(texts: list[str]) -> np.ndarray:
    """1 = contains a non-negated gambling marker."""
    return np.array([1 if score_text(t).gambling_hits > 0 else 0 for t in texts])


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
    cv_auc: float
    novel_candidates: list[tuple[str, float]]  # texts the lexicon missed


def train_and_report(texts: list[str], top_novel: int = 10,
                     cv: int = 5) -> tuple[Pipeline, WeakSupervisionReport]:
    """Fit on weak labels; return model + CV AUC and lexicon-missed candidates."""
    y = weak_labels(texts)
    model = build_model()

    proba = cross_val_predict(model, texts, y, cv=cv, method="predict_proba")[:, 1]
    auc = roc_auc_score(y, proba)

    model.fit(texts, y)
    scores = model.predict_proba(texts)[:, 1]
    novel = [
        (t, float(s)) for t, s, label in zip(texts, scores, y)
        if label == 0 and score_text(t).gambling_hits == 0
    ]
    novel.sort(key=lambda x: -x[1])

    report = WeakSupervisionReport(
        n_docs=len(texts),
        n_positive=int(y.sum()),
        cv_auc=float(auc),
        novel_candidates=novel[:top_novel],
    )
    return model, report
