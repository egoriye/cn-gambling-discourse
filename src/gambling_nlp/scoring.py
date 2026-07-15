"""Lexicon-based gambling-propensity scoring for Chinese texts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

import jieba

from .lexicon import LEXICON, GAMBLING_CATEGORIES, RESTRAINT_CATEGORY, all_terms

for _term in all_terms():
    jieba.add_word(_term)

_TERM2CAT = all_terms()

NEGATORS = {"不", "没", "没有", "别", "勿", "不要", "拒绝", "从不", "绝不"}
NEGATION_WINDOW = 2


@dataclass
class ScoreResult:
    """Result of scoring a single document."""

    n_tokens: int
    hits: Counter = field(default_factory=Counter)          # term -> count
    category_counts: Counter = field(default_factory=Counter)  # category -> count
    negated: Counter = field(default_factory=Counter)       # negated term -> count

    @property
    def gambling_hits(self) -> int:
        return sum(self.category_counts[c] for c in GAMBLING_CATEGORIES)

    @property
    def restraint_hits(self) -> int:
        return self.category_counts[RESTRAINT_CATEGORY]

    @property
    def gambling_score(self) -> float:
        """Gambling-marker density per 100 tokens."""
        if self.n_tokens == 0:
            return 0.0
        return 100.0 * self.gambling_hits / self.n_tokens

    @property
    def restraint_score(self) -> float:
        """Restraint-marker density per 100 tokens."""
        if self.n_tokens == 0:
            return 0.0
        return 100.0 * self.restraint_hits / self.n_tokens

    @property
    def net_score(self) -> float:
        """Gambling density minus restraint density, per 100 tokens."""
        return self.gambling_score - self.restraint_score


def tokenize(text: str) -> list[str]:
    """jieba segmentation, whitespace dropped."""
    return [t for t in jieba.lcut(text) if t.strip()]


def score_text(text: str) -> ScoreResult:
    """Score a single document against the lexicon."""
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
