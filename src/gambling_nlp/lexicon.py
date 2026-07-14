"""Seed lexicon of gambling-discourse markers in Chinese investor texts.

Categories map to constructs from the behavioural-finance literature on
lottery-like stock preference and loss chasing in the Chinese market.
"""

from __future__ import annotations

LEXICON: dict[str, list[str]] = {
    "GAMBLING_CORE": [
        "赌博", "赌徒", "赌局", "赌注", "博彩", "彩票", "中奖", "开奖",
        "赌一把", "赌一波", "押注", "下注", "买彩票", "福利彩票", "体育彩票",
        "快乐8", "麻将", "打麻将", "抽奖", "六合彩", "小赌怡情",
    ],
    "SPECULATION": [
        "以小博大", "梭哈", "梭了", "全仓", "满仓", "重仓", "加杠杆",
        "上杠杆", "一夜暴富", "暴富", "翻倍", "十倍股", "搏一搏",
        "富贵险中求", "单车变摩托", "赌性",
    ],
    "LOSS_CHASING": [
        "回本", "翻身", "扳回", "补仓", "越跌越买", "抄底", "解套",
        "回血", "拉低成本", "不服", "再来一把",
    ],
    "LOTTERY_STOCK": [
        "涨停", "打板", "追涨", "妖股", "题材股", "概念股", "龙头股",
        "连板", "涨停板", "低价股", "仙股",
    ],
    "CONFUCIAN_RESTRAINT": [
        "稳健", "保守", "止损", "分散", "长期持有", "价值投资",
        "理性", "勤俭", "节制", "风险控制", "定投",
    ],
}

GAMBLING_CATEGORIES = (
    "GAMBLING_CORE",
    "SPECULATION",
    "LOSS_CHASING",
    "LOTTERY_STOCK",
)

RESTRAINT_CATEGORY = "CONFUCIAN_RESTRAINT"


def all_terms() -> dict[str, str]:
    """Return a flat mapping ``term -> category``."""
    flat: dict[str, str] = {}
    for category, terms in LEXICON.items():
        for term in terms:
            flat[term] = category
    return flat
