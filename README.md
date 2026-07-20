# cn-gambling-discourse

[![tests](https://github.com/egoriye/cn-gambling-discourse/actions/workflows/ci.yml/badge.svg)](https://github.com/egoriye/cn-gambling-discourse/actions)

Python toolkit for counting gambling-register vocabulary in Chinese-language financial texts (stock-forum posts, comments, news). Developed as part of a study of the historical gambling culture of China and its role in the financial behaviour of the contemporary PRC population.

The output of the toolkit is a measure of text. It reports how much gambling-register vocabulary a document contains (gambling-discourse density). It does not support conclusions about the disposition of the author. Section "Scope of the measure" below states the reasons; RESULTS.md documents what the pilot corpora do and do not show.

## Lexicon structure

A dictionary of gambling-related vocabulary applied to a stock forum will mostly match ordinary trading vocabulary. Terms such as 涨停 ("limit-up"), 满仓 ("full position") and 抄底 ("buy the dip") occur in the writing of cautious and speculative investors alike and indicate the topic of the text rather than any property of the writer. On the pilot corpora, a lexicon that counts such terms as gambling markers flags 7.1% of documents; with those terms moved to a separate tier, the figure is 0.0% (RESULTS.md).

The lexicon therefore contains 69 simplified-Chinese terms in four tiers. Only the first two count toward the gambling score.

| Tier | Examples | In score |
|---|---|---|
| GAMBLING_EXPLICIT | 赌博 gambling, 彩票 lottery ticket, 开奖 prize draw, 麻将 mahjong | yes |
| GAMBLING_FRAMING | 以小博大 small stake big win, 梭哈 all-in, 一夜暴富 rich overnight | yes |
| TRADING_MECHANICS | 涨停 limit-up, 满仓 full position, 抄底 buy the dip | no (tracked separately) |
| RESTRAINT | 稳健 prudent, 止损 stop-loss, 价值投资 value investing | counter-register |

Each term has an English gloss in `GLOSSES`.

## Functionality

- Segmentation with [jieba](https://github.com/fxsjy/jieba); multi-character lexicon terms are registered in the segmenter dictionary.
- Per-document marker densities (hits per 100 tokens) for each tier. A negation window suppresses matches preceded within two tokens by 不, 没, 别, 勿 or fused forms (从来不), so that 不加杠杆 "no leverage" is not counted.
- `gambling_nlp.classifier`: weak supervision. Documents with a hit in a chosen tier are used as positive labels for a character-n-gram TF-IDF + logistic regression model; documents with no seed term that receive high scores are candidates for lexicon expansion. If a tier has too few positives for cross-validation, the module reports this instead of fitting a model.
- `scripts/build_index.py`: aggregation into a daily index for corpora with timestamps.
- `scripts/pilot_analysis.py`: reproduces all figures in RESULTS.md; downloads the pilot corpora on first run.

## Installation and usage

```bash
pip install -e ".[dev]"
python -m gambling_nlp.cli data/demo_posts.csv
python -m pytest tests/
```

Browser demo (substring matching only, no segmentation): https://egoriye.github.io/cn-gambling-discourse/

## Scope of the measure

Density of gambling-register vocabulary in a text is separated from any claim about the writer by three problems, none of which word counting resolves.

1. Chinese business usage includes gambling-derived idiom (黑马 "dark horse", 井喷 "gusher", 一夜暴富 "rich overnight"). A higher count may reflect the phraseology of the language rather than a property of the writer. Assessing a writer's choice requires the base rate of these constructions in general Chinese.
2. Community slang (the Chinese counterpart of WallStreetBets vocabulary) identifies a written register. A register can be adopted ironically or performatively, so detecting it establishes usage, and usage alone.
3. The outcomes discussed in the behavioural-finance literature (lottery-stock overpricing, crash risk) concern trading. Connecting discourse to trading requires market data in addition to text.

Designs that address each problem in turn are listed in the accompanying preprint (baseline-corrected density against a general corpus; human annotation of register; alignment with volatility and price data). None is implemented here.

## Limitations

Tier assignment involves judgement calls (妖股 "monster stock" is kept in TRADING_MECHANICS); the tiers are versioned so the assignment can be changed and the effect measured. Lexicon matching does not handle irony, quotation or reported speech. Classifier AUC is computed against lexicon-derived labels and measures internal consistency only. All reported quantities are descriptive densities.

## License

MIT
