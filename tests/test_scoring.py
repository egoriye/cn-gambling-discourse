from gambling_nlp import score_text, score_corpus


def test_gambling_text_scores_positive():
    res = score_text("满仓梭哈这只妖股，以小博大，赌一把！")
    assert res.gambling_hits >= 4
    assert res.net_score > 0


def test_restraint_text_scores_negative():
    res = score_text("坚持价值投资，长期持有，止损分散，稳健理性。")
    assert res.restraint_hits >= 4
    assert res.net_score < 0


def test_empty_text():
    res = score_text("")
    assert res.n_tokens == 0
    assert res.gambling_score == 0.0


def test_negation_is_not_counted():
    res = score_text("我从来不加杠杆，也不赌博。")
    assert res.gambling_hits == 0
    assert sum(res.negated.values()) >= 2


def test_negated_leverage_not_counted():
    res = score_text("市场波动太大，我选择分散配置，保守理性，不加杠杆。")
    assert res.gambling_hits == 0
    assert "加杠杆" in res.negated


def test_category_counts():
    res = score_text("满仓梭哈这只妖股，以小博大，赌一把！")
    assert res.category_counts["SPECULATION"] >= 2
    assert res.category_counts["LOTTERY_STOCK"] >= 1
    assert res.category_counts["GAMBLING_CORE"] >= 1


def test_score_corpus():
    texts = ["赌一把", "稳健止损"]
    results = score_corpus(texts)
    assert len(results) == 2
    assert results[0].gambling_hits >= 1
    assert results[1].restraint_hits >= 1
