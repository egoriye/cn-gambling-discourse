"""Tiered lexicon scoring for Chinese investor texts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

import jieba

from .lexicon import (
    GAMBLING_CATEGORIES,
    MECHANICS_CATEGORY,
    RESTRAINT_CATEGORY,
    all_terms,
)

for _term in all_terms():
    jieba.add_word(_term)

_TERM2CAT = all_terms()

NEGATORS = {"不", "没", "没有", "别", "勿", "不要", "拒绝", "从不", "绝不"}
NEGATION_WINDOW = 2


@dataclass
class ScoreResult:
    """Result of scoring a single document."""

    n_tokens: int
    hits: Counter = field(default_factory=Counter)
    category_counts: Counter = field(default_factory=Counter)
    negated: Counter = field(default_factory=Counter)

    @property
    def gambling_hits(self) -> int:
        """Overtly gambling-marked hits; excludes trading mechanics."""
        return sum(self.category_counts[c] for c in GAMBLING_CATEGORIES)

    @property
    def mechanics_hits(self) -> int:
        return self.category_counts[MECHANICS_CATEGORY]

    @property
    def restraint_hits(self) -> int:
        return self.category_counts[RESTRAINT_CATEGORY]

    def _density(self, n: int) -> float:
        return 0.0 if self.n_tokens == 0 else 100.0 * n / self.n_tokens

    @property
    def gambling_score(self) -> float:
        return self._density(self.gambling_hits)

    @property
    def mechanics_score(self) -> float:
        """Trading-topic density; a genre control, not a gambling measure."""
        return self._density(self.mechanics_hits)

    @property
    def restraint_score(self) -> float:
        return self._density(self.restraint_hits)

    @property
    def net_score(self) -> float:
        """Gambling density minus restraint density, per 100 tokens."""
        return self.gambling_score - self.restraint_score


def tokenize(text: str) -> list[str]:
    """jieba segmentation, whitespace dropped."""
    return [t for t in jieba.lcut(text) if t.strip()]


def score_text(text: str) -> ScoreResult:
    """Score a single document against the tiered lexicon."""
    tokens = tokenize(text)
    result = ScoreResult(n_tokens=len(tokens))
    for i, token in enumerate(tokens):
        category = _TERM2CAT.get(token)
        if category is None:
            continue
        window = tokens[max(0, i - NEGATION_WINDOW):i]
        if any(w in NEGATORS or w.endswith(("不", "没", "别", "勿")) for w in window):
            result.negated[token] += 1
            continue
        result.hits[token] += 1
        result.category_counts[category] += 1
    return result


def score_corpus(texts: list[str]) -> list[ScoreResult]:
    """Score a list of documents."""
    return [score_text(t) for t in texts]
