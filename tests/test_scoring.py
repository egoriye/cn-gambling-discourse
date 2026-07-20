from gambling_nlp import score_text
from gambling_nlp.lexicon import GLOSSES, all_terms


def test_explicit_gambling_scores_positive():
    res = score_text("赌一把，以小博大，一夜暴富！")
    assert res.gambling_hits >= 3
    assert res.net_score > 0


def test_restraint_text_scores_negative():
    res = score_text("坚持价值投资，长期持有，止损分散，稳健理性。")
    assert res.restraint_hits >= 4
    assert res.net_score < 0


def test_trading_mechanics_are_not_gambling():
    res = score_text("满仓抄底这只涨停的妖股，准备补仓解套。")
    assert res.mechanics_hits >= 4
    assert res.gambling_hits == 0
    assert res.gambling_score == 0.0


def test_negation_is_not_counted():
    res = score_text("我从来不赌博，也不押注。")
    assert res.gambling_hits == 0
    assert sum(res.negated.values()) >= 2


def test_empty_text():
    res = score_text("")
    assert res.n_tokens == 0
    assert res.gambling_score == 0.0


def test_every_term_has_a_gloss():
    assert set(all_terms()) == set(GLOSSES)


def test_mechanics_and_gambling_are_disjoint():
    from gambling_nlp.lexicon import LEXICON, GAMBLING_CATEGORIES, MECHANICS_CATEGORY
    marked = {t for c in GAMBLING_CATEGORIES for t in LEXICON[c]}
    assert not (marked & set(LEXICON[MECHANICS_CATEGORY]))

