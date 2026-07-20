import pytest

pytest.importorskip("sklearn")

from gambling_nlp.classifier import train_and_report, weak_labels


def test_weak_labels_use_the_gambling_tier_only():
    texts = ["满仓抄底涨停妖股", "赌一把，以小博大"]
    y = weak_labels(texts)
    assert list(y) == [0, 1]


def test_sparse_tier_reports_instead_of_training():
    texts = ["价值投资长期持有"] * 40 + ["赌一把"]
    model, rep = train_and_report(texts)
    assert model is None
    assert rep.cv_auc is None
    assert "too sparse" in rep.note
