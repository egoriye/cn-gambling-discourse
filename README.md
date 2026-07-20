[![tests](https://github.com/egoriye/cn-gambling-discourse/actions/workflows/ci.yml/badge.svg)](https://github.com/egoriye/cn-gambling-discourse/actions)

**A tool for measuring the density of gambling *discourse* in Chinese investor texts — and an explicit account of why that is not the same as measuring how gambling-prone the writers are.**

The toolkit counts gambling-register vocabulary in Chinese-language financial texts (stock-forum posts, comments, news). It grew out of a study of the historical gambling culture of China as a Williamson level-1 informal institution and its reproduction in contemporary financial behaviour. The central design commitment is honesty about what a word count can and cannot support.

## What this measures — and what it does not

This tool measures a property of **text**: how much gambling-register vocabulary a document contains. It does **not** measure a property of **people**: how gambling-prone the author is. Three gaps separate the two, and none is crossed by counting words:

1. **Language ≠ speaker.** Chinese is rich in gambling-derived idiom (黑马 "dark horse", 井喷 "gusher", 一夜暴富 "rich overnight"). A writer may use more of it simply by writing idiomatic Chinese, not by being more of a gambler. Higher density can mean a richer gambling phraseology in the *language*, not a more gambling-prone *author*.
2. **Register ≠ disposition.** Even community slang (the Chinese analogue of WSB's *YOLO*, *diamond hands*) shows that a writer adopts a register. Register is a performance; an ironic analyst can write "YOLO". Talking like a gambler is not being one.
3. **Speech ≠ behaviour.** A writer sincerely gambling in speech need not trade that way. The crash-risk outcomes the underlying theory cares about are behavioural, not lexical.

Accordingly the honest name for the output is **gambling-discourse density**, not "gambling propensity". The tool is the first link in a chain, not the whole chain. See [RESULTS.md](RESULTS.md) for what the pilot does and does not show.

## The tiering, and why it matters

A dictionary of "gambling-related vocabulary" applied to a stock forum mostly finds *trading* vocabulary. 涨停 ("limit-up"), 满仓 ("full position") and 抄底 ("buy the dip") are said by prudent and reckless investors alike — they report the topic, not the writer. The lexicon is therefore tiered, and only disposition-marking tiers count toward the score:

| Tier | Examples | Counted? |
|---|---|---|
| `GAMBLING_EXPLICIT` | 赌博 gambling, 彩票 lottery ticket, 开奖 prize draw, 麻将 mahjong | yes |
| `GAMBLING_FRAMING` | 以小博大 small stake big win, 梭哈 all-in, 一夜暴富 rich overnight | yes |
| `TRADING_MECHANICS` | 涨停 limit-up, 满仓 full position, 抄底 buy the dip | no — topic control |
| `RESTRAINT` | 稳健 prudent, 止损 stop-loss, 价值投资 value investing | counter-register |

On the pilot corpora, an untiered lexicon reports gambling discourse in 7.1% of documents; separating the tiers drops it to 0.0% — every hit was trading vocabulary. That contamination result is the point: any text measure of gambling must clear this bar before its numbers mean anything, and even then only measures discourse.

Every term carries an English gloss (`GLOSSES`), so output is readable without Chinese.

## What it does

- Segments Chinese text with [jieba](https://github.com/fxsjy/jieba), keeping multi-character terms intact.
- Scores each document as marker density per 100 tokens, per tier, with a negation window (不加杠杆 "no leverage" is not counted).
- `gambling_nlp.classifier` uses a tier as a weak labeller to train a char-n-gram classifier, ranks documents with no seed term as expansion candidates, and reports rather than trains when a tier is too sparse.
- `scripts/build_index.py` aggregates a daily discourse index for timestamped corpora.

## Quick start

```bash
pip install -e ".[dev]"
python -m gambling_nlp.cli data/demo_posts.csv
python -m pytest tests/
```

Or in the browser: **https://egoriye.github.io/cn-gambling-discourse/**

## What the tool enables (research programme)

Because it isolates a discourse measure, the tool supports designs that begin to close the three gaps — none claimed here, all left as future work:

1. **Baseline-corrected density** (gap 1): compare gambling-idiom density in investor text against its base rate in general Chinese, isolating the writer's choice from the language's stock of idiom.
2. **Cross-volatility** (toward gap 3): discourse density across boards of high- vs low-volatility stocks, holding genre fixed.
3. **Cross-register / cross-language** (gap 2): retail forum vs formal news vs a matched English lexicon — is gambling framing specific to a community, a genre, or a language?
4. **Applied**: crypto-forum and financial-marketing text, where the same measurement problem recurs.

## Limitations

Tier assignment is a judgement call, versioned so the line can be moved and its effect measured. Matching does not resolve irony, quotation, or reported speech. Classifier AUC is against lexicon-derived labels (internal consistency, not accuracy vs human judgement). Scores are descriptive densities, not calibrated probabilities, and never a measure of persons.

## License

MIT
