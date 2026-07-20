# Pilot results

Two public Eastmoney Guba sample corpora from [IVTz/GubaScraper](https://github.com/IVTz/GubaScraper),
scored with `gambling_nlp` v0.2.0, exact duplicates removed.
Reproduce: `python scripts/pilot_analysis.py`.

| Corpus | Docs | Tokens | Gambling-marked | Trading mechanics | Restraint |
|---|---|---|---|---|---|
| Titles, 600519 (Kweichow Moutai), 2001–2012 | 970 | 11,814 | **0 (0.0%)** | 68 (7.0%) | 3 (0.3%) |
| Replies, 300343, 2015–2022 | 1,161 | 12,399 | **4 (0.3%)** | 27 (2.3%) | 3 (0.3%) |

## What this shows

**1. The contamination result.** An untiered lexicon reports gambling discourse in
7.1% of the title corpus. Separating disposition-marking vocabulary from trading
mechanics drops this to 0.0%: every apparent hit was 涨停 (34), 全仓 (25), 满仓 (6) —
limit-ups and position sizes. A dictionary that counts these measures what a forum
is *about*, not how its users think.

**2. The seed lexicon does not fit forum text.** The gambling tier is built from the
vocabulary of the cultural-historical record (赌博, 彩票, 麻将, 以小博大). Investors do
not write in that register; they write 暴涨 ("surge"), 井喷 ("gusher"), 黑马 ("dark
horse"). Overtly gambling-marked discourse appears in 4 of 2,131 documents (0.2%),
and of 8 occurrences of 开奖 ("prize draw"), 6 are one copy-pasted message — so the
most quotable stock-as-lottery instance is boilerplate.

## What this does NOT show

This pilot does **not** show that Chinese investors are not gambling-prone, nor that
distinguishing vocabulary does not exist. It shows three narrower things:

- historical gambling vocabulary is nearly absent from these forums;
- naively widening the lexicon to fit (adding 牛股, 黑马, 暴涨) captures ordinary
  business jargon, not disposition — the same topic-vs-disposition error one tier down;
- the two corpora chosen are close to worst-case for the question: 600519 is China's
  archetypal value stock (long-term holders), and the titles predate modern forum
  slang.

Above all, **even a non-zero, well-behaved density would measure discourse, not
persons.** Three gaps stand between the two — language vs speaker, register vs
disposition, speech vs behaviour (see README and the preprint) — and none is crossed
by counting words. These numbers describe text.

## Where the register actually lives (lead for v2)

Trained on the mechanics tier (95 positives, 5-fold CV ROC-AUC 0.865), the classifier
ranks zero-seed-term documents; the top candidates are promotional — 要涨3倍 ("will
triple"), 翻番利器 ("doubling weapon"), 井喷 ("gusher"), 暴涨. In these corpora the
jackpot register is carried by pump vocabulary, not by the classical gambling lexicon.
This is a lead for lexicon iteration, not evidence about investors.

## Caveats

Small samples; two boards; different periods and genres; a blue chip and a small cap.
Not comparable to each other; no causal claim; nothing here generalises to Chinese
investors.
