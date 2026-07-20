"""gambling_nlp — lexicon-based detection of gambling discourse in Chinese retail-investor texts."""

from .lexicon import (LEXICON, GAMBLING_CATEGORIES, MECHANICS_CATEGORY,
                      RESTRAINT_CATEGORY, GLOSSES, gloss)
from .scoring import score_text, score_corpus, tokenize, ScoreResult

__all__ = [
    "LEXICON", "GAMBLING_CATEGORIES", "MECHANICS_CATEGORY", "RESTRAINT_CATEGORY",
    "GLOSSES", "gloss",
    "score_text", "score_corpus", "tokenize", "ScoreResult",
]
__version__ = "0.2.0"
