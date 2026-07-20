"""Seed lexicon for gambling discourse in Chinese investor texts.

The lexicon is tiered, because not every gambling-flavoured word in a
stock forum reports a gambling disposition.  Standard trading vocabulary
(涨停 "limit-up", 满仓 "full position", 抄底 "buy the dip") describes market
mechanics and is used by prudent and speculative investors alike; counting
it as gambling discourse measures topic, not disposition.  Such terms are
kept in a ``TRADING_MECHANICS`` tier that is tracked but excluded from the
gambling score.

Tiers:
    GAMBLING_EXPLICIT  - literal gambling and lottery vocabulary
    GAMBLING_FRAMING   - figurative gambling framing of trading
    TRADING_MECHANICS  - standard trading vocabulary (topic control)
    RESTRAINT          - prudence vocabulary (counter-register)
"""

from __future__ import annotations

LEXICON: dict[str, list[str]] = {
    "GAMBLING_EXPLICIT": [
        "赌博", "赌徒", "赌局", "赌注", "博彩", "彩票", "中奖", "开奖",
        "赌一把", "赌一波", "押注", "下注", "买彩票", "福利彩票", "体育彩票",
        "快乐8", "麻将", "打麻将", "抽奖", "六合彩", "小赌怡情",
    ],
    "GAMBLING_FRAMING": [
        "以小博大", "梭哈", "梭了", "一夜暴富", "暴富", "搏一搏",
        "富贵险中求", "单车变摩托", "赌性", "再来一把",
    ],
    "TRADING_MECHANICS": [
        "涨停", "涨停板", "打板", "追涨", "连板", "妖股", "题材股",
        "概念股", "龙头股", "低价股", "仙股", "满仓", "全仓", "重仓",
        "加杠杆", "上杠杆", "翻倍", "十倍股", "抄底", "补仓", "解套",
        "回本", "翻身", "扳回", "回血", "拉低成本", "越跌越买",
    ],
    "RESTRAINT": [
        "稳健", "保守", "止损", "分散", "长期持有", "价值投资",
        "理性", "勤俭", "节制", "风险控制", "定投",
    ],
}

GAMBLING_CATEGORIES = ("GAMBLING_EXPLICIT", "GAMBLING_FRAMING")
MECHANICS_CATEGORY = "TRADING_MECHANICS"
RESTRAINT_CATEGORY = "RESTRAINT"

GLOSSES: dict[str, str] = {
    "赌博": "gambling", "赌徒": "gambler", "赌局": "gambling game",
    "赌注": "stake", "博彩": "gaming/lottery", "彩票": "lottery ticket",
    "中奖": "win a prize", "开奖": "prize draw", "赌一把": "have a gamble",
    "赌一波": "take a gamble", "押注": "place a bet", "下注": "place a bet",
    "买彩票": "buy lottery tickets", "福利彩票": "welfare lottery",
    "体育彩票": "sports lottery", "快乐8": "Happy-8 (lottery game)",
    "麻将": "mahjong", "打麻将": "play mahjong", "抽奖": "lucky draw",
    "六合彩": "Mark Six lottery", "小赌怡情": "a small bet does no harm",
    "以小博大": "small stake, big win", "梭哈": "all-in (show hand)",
    "梭了": "went all-in", "一夜暴富": "rich overnight", "暴富": "get rich quick",
    "搏一搏": "take a shot", "富贵险中求": "fortune favours the bold",
    "单车变摩托": "bike into a motorbike (small win to big)",
    "赌性": "gambling instinct", "再来一把": "one more round",
    "涨停": "limit-up", "涨停板": "limit-up board", "打板": "chase the limit-up",
    "追涨": "chase the rally", "连板": "consecutive limit-ups",
    "妖股": "monster stock", "题材股": "theme stock", "概念股": "concept stock",
    "龙头股": "leading stock", "低价股": "low-priced stock", "仙股": "penny stock",
    "满仓": "fully invested", "全仓": "full position", "重仓": "heavy position",
    "加杠杆": "add leverage", "上杠杆": "use leverage", "翻倍": "double",
    "十倍股": "ten-bagger", "抄底": "buy the dip", "补仓": "average down",
    "解套": "get out of a losing position", "回本": "recover the principal",
    "翻身": "turn things around", "扳回": "win it back", "回血": "recover losses",
    "拉低成本": "lower the cost basis", "越跌越买": "buy more as it falls",
    "稳健": "prudent", "保守": "conservative", "止损": "stop-loss",
    "分散": "diversify", "长期持有": "hold long-term", "价值投资": "value investing",
    "理性": "rational", "勤俭": "thrifty", "节制": "moderation",
    "风险控制": "risk control", "定投": "regular investment plan",
}


def gloss(term: str) -> str:
    """English gloss for a lexicon term."""
    return GLOSSES.get(term, "")


def all_terms() -> dict[str, str]:
    """Return a flat mapping ``term -> category``."""
    flat: dict[str, str] = {}
    for category, terms in LEXICON.items():
        for term in terms:
            flat[term] = category
    return flat
