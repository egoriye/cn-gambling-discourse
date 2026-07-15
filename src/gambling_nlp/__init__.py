"""gambling_nlp — lexicon-based detection of gambling discourse in Chinese retail-investor texts."""

from .lexicon import LEXICON, GAMBLING_CATEGORIES, RESTRAINT_CATEGORY
from .scoring import score_text, score_corpus, tokenize, ScoreResult

__all__ = [
    "LEXICON", "GAMBLING_CATEGORIES", "RESTRAINT_CATEGORY",
    "score_text", "score_corpus", "tokenize", "ScoreResult",
]
__version__ = "0.1.0"
