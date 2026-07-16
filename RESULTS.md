# Pilot results

Two publicly available sample corpora of Eastmoney Guba texts, distributed
with the open-source scraper [IVTz/GubaScraper](https://github.com/IVTz/GubaScraper),
were scored with `gambling_nlp` (v0.1.0). Exact duplicate documents were removed.
Reproduce with `python scripts/pilot_analysis.py`.

| Corpus | Docs | Tokens | Docs w/ gambling marker | Docs w/ restraint marker | Gambling density /100 tok | Restraint density /100 tok |
|---|---|---|---|---|---|---|
| Post titles, board 600519 (Kweichow Moutai), 2001–2012 | 970 | 11,814 | 69 (7.1%) | 3 (0.3%) | 0.63 | 0.03 |
| Replies, board 300343, 2022 | 1,161 | 12,399 | 33 (2.8%) | 3 (0.3%) | 0.31 | 0.02 |

## Observations

1. **Asymmetry.** In both corpora gambling-discourse markers outnumber
   Confucian-restraint markers by an order of magnitude (~20:1 at the
   document level), consistent with the characterisation of retail-investor
   forums as a speculation-dominated discourse environment.
2. **Different gambling profiles.** The blue-chip title corpus is dominated
   by limit-up chasing and all-in vocabulary (涨停 ×35, 全仓 ×25 —
   `LOTTERY_STOCK` + `SPECULATION`), whereas the 2022 reply corpus is
   dominated by loss-chasing vocabulary (抄底, 解套, 回本 — `LOSS_CHASING`),
   the "win it back" pattern described in the behavioural-finance literature.
3. **Literal lottery metaphors.** Replies include direct lottery-draw
   framing of stock outcomes, e.g. 马上开奖，祝您好运 ("the draw is coming,
   good luck") — investors describing equity positions in the vocabulary of
   a lottery ticket.

## Weak-supervision classifier

Using lexicon hits as weak labels (99 positives / 2,131 docs), a char-2-4-gram
TF-IDF + logistic regression achieves **5-fold CV ROC-AUC 0.867**. The fitted
model's highest-scored documents *without any seed term* are dominated by
pump-style discourse (要涨3倍 "will triple", 翻番利器 "doubling weapon",
报复性井喷上涨 "vengeful gusher rally") — evidence that the classifier
generalises beyond the seed dictionary and can drive lexicon expansion.

## Daily Gambling Discourse Index

`scripts/build_index.py` produces `data/pilot/daily_gdi.csv` — 361 trading-day
observations (2015–2022) of gambling-marker density for board 300343.

## Caveats

- Small pilot samples covering two boards, different periods and genres
  (titles vs. replies); the two corpora are **not** directly comparable and
  no causal claims are made.
- Lexicon matching applies a short negation window but does not handle
  irony or sarcasm; scores are descriptive densities.
- Scale-up path: apply the pipeline to a large public corpus such as the
  SSE 50 Guba comment dataset (ScienceDB, 2020) or a purpose-built crawl.
