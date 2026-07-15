import pytest

sklearn = pytest.importorskip("sklearn")

from gambling_nlp import score_text
from gambling_nlp.classifier import train_and_report, weak_labels


def test_weak_labels_from_lexicon():
    texts = [
        "满仓梭哈这只妖股",
        "坚持价值投资，长期持有",
        "今天天气不错",
    ]
    y = weak_labels(texts)
    assert y.tolist() == [1, 0, 0]


def test_train_and_report_smoke():
    texts = [
        "满仓梭哈这只妖股，赌一把",
        "梭哈全仓打板涨停",
        "坚持价值投资，止损分散",
        "稳健理性，长期持有",
        "今天市场波动不大",
        "这只票要涨三倍，翻番利器",
        "报复性井喷上涨，兄弟们冲",
        "继续观望，没有操作",
    ] * 3
    model, report = train_and_report(texts, top_novel=3, cv=3)
    assert report.n_docs == len(texts)
    assert report.n_positive > 0
    assert 0.5 <= report.cv_auc <= 1.0
    assert model.predict_proba(texts[:1]).shape == (1, 2)
    assert all(score_text(t).gambling_hits == 0 for t, _ in report.novel_candidates)
