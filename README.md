# cn-gambling-discourse

[![tests](https://github.com/egoriye/cn-gambling-discourse/actions/workflows/ci.yml/badge.svg)](https://github.com/egoriye/cn-gambling-discourse/actions)

**A measurement toolkit for gambling discourse in Chinese retail-investor texts: seed lexicon, negation-aware scoring, weakly-supervised classifier, daily Gambling Discourse Index (GDI).**

A lightweight NLP toolkit that measures the density of gambling-related vocabulary in Chinese-language financial texts (stock-forum posts, investor comments, news). It operationalises findings from behavioural-finance research on the Chinese stock market — lottery-like stock preference (the MAX anomaly), the *yi xiao bo da* (以小博大, "small stake, big win") logic, and loss-chasing behaviour — as a reproducible text-analysis pipeline.

The project grew out of an interdisciplinary study of the historical gambling culture of China as a Williamson level-1 informal institution and its reproduction in the financial behaviour of the contemporary PRC population.

## Why

Empirical work on gambling culture and Chinese stock-market behaviour measures
regional gambling propensity through lottery sales — a coarse, province-level,
low-frequency proxy. This toolkit provides a *text-based* alternative in the
tradition of dictionary-derived indices in economics and finance (cf. the
Economic Policy Uncertainty index of Baker–Bloom–Davis and the
Loughran–McDonald financial sentiment dictionary): a transparent frequency
measure computable per stock, per day, or per user.

## What it does

- Segments Chinese text with [jieba](https://github.com/fxsjy/jieba), keeping multi-character lexicon terms intact.
- Matches tokens against a five-category lexicon:

| Category | Examples | Interpretation |
|---|---|---|
| `GAMBLING_CORE` | 赌博, 彩票, 快乐8, 麻将 | explicit gambling / lottery vocabulary |
| `SPECULATION` | 以小博大, 梭哈, 全仓, 一夜暴富 | all-in, jackpot-seeking trading slang |
| `LOSS_CHASING` | 回本, 翻身, 补仓, 再来一把 | "win it back" vocabulary |
| `LOTTERY_STOCK` | 涨停, 打板, 妖股, 连板 | lottery-like stock discourse |
| `CONFUCIAN_RESTRAINT` | 稳健, 止损, 价值投资, 定投 | prudence counter-institution vocabulary |

- Applies a negation window (不 / 没 / 别 / 勿 and derivatives), so 不加杠杆
  ("no leverage") is not counted as gambling discourse.
- Computes per-document scores: gambling-marker density and restraint-marker density (per 100 tokens), and a **net score** capturing the opposition between the gambling institution and its Confucian counter-institution.

## Beyond the lexicon: weak supervision

`gambling_nlp.classifier` uses the lexicon as a *weak labeller* and trains a
character-n-gram TF-IDF + logistic-regression model on those labels
(5-fold CV ROC-AUC **0.867** on the pilot corpora). The trained model flags
gambling-toned documents containing **none** of the seed terms — e.g.
pump-style posts built on 暴涨 / 井喷 / 翻番 vocabulary — turning the static
dictionary into an expandable annotation loop (model-ranked candidates →
human review → lexicon v2).

## Daily index

`scripts/build_index.py` aggregates scores into a daily **Gambling Discourse
Index** (gambling hits per 100 tokens per day) — a time series that can be
laid alongside price and volume data.

## Live demo

Try the browser demo (paste any Chinese text, see highlighted markers and the score):
**https://egoriye.github.io/cn-gambling-discourse/**

## Quick start

```bash
pip install -e .
python -m gambling_nlp.cli data/demo_posts.csv
```

Or from Python:

```python
from gambling_nlp import score_text

res = score_text("满仓梭哈这只妖股，以小博大，赌一把！")
print(res.gambling_score, res.net_score, dict(res.hits))
```

Input for the CLI is any UTF-8 CSV with a text column (`--text-column`, default `text`). The output CSV appends token counts, category hits, densities, and the matched terms for full transparency.

`data/demo_posts.csv` contains **synthetic demo sentences** for testing the pipeline; it is not research data.

## Applications

- Constructing a text-based regional or temporal gambling-propensity index from stock-forum corpora (e.g., Eastmoney Guba), as a complement to the lottery-sales proxy widely used in the empirical literature.
- Filtering and annotating corpora for downstream supervised classification of speculative vs. prudent investor discourse.

## Limitations

- Pure lexicon matching: negation (不加杠杆 "no leverage") is not handled and inflates scores; a rule-based negation window or a supervised classifier is the natural next step.
- The lexicon reflects mainland simplified-Chinese investor slang of the 2010s–2020s; coverage of Cantonese and traditional-script communities is limited.
- Scores are descriptive densities, not calibrated probabilities.

## Pilot results

See [RESULTS.md](RESULTS.md) — the pipeline applied to two public Guba sample corpora (~2,100 real documents), reproducible via `python scripts/pilot_analysis.py`.

## Tests

```bash
pip install -e ".[dev]"
python -m pytest tests/
```

## License

MIT

## Citation

If you use this toolkit, please cite the accompanying preprint (link to be added upon posting).
