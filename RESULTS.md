# Pilot results

Two publicly available sample corpora of Eastmoney Guba texts, distributed with the scraper [IVTz/GubaScraper](https://github.com/IVTz/GubaScraper), scored with `gambling_nlp` v0.2.0 after removal of exact duplicates. To reproduce: `python scripts/pilot_analysis.py`.

| Corpus | Docs | Tokens | Gambling-marked | Trading mechanics | Restraint |
|---|---|---|---|---|---|
| Titles, board 600519 (Kweichow Moutai), 2001–2012 | 970 | 11,814 | 0 (0.0%) | 68 (7.0%) | 3 (0.3%) |
| Replies, board 300343, 2015–2022 | 1,161 | 12,399 | 4 (0.3%) | 27 (2.3%) | 3 (0.3%) |

## Effect of the tier separation

A lexicon that counts trading vocabulary as gambling markers flags 7.1% of the title corpus. With the TRADING_MECHANICS tier excluded from the score, the gambling tiers flag 0.0%. All apparent hits in the title corpus were 涨停 (34), 全仓 (25), 满仓 (6) and similar terms. The corresponding figures for the reply corpus are 2.8% and 0.3%.

The untiered version also produces a roughly 20:1 ratio of gambling to restraint vocabulary. Since the gambling side of that ratio consists of trading terms, the ratio reflects the subject matter of a stock forum. A gambling measure that has cleared this problem still remains a measure of text; see "Scope of the measure" in the README.

## Fit between the seed lexicon and forum text

The gambling tiers draw on the vocabulary of the historical record (赌博, 彩票, 麻将, 以小博大). This vocabulary is nearly absent from the pilot corpora: 4 documents out of 2,131 contain a gambling-tier term. Of 8 raw occurrences of 开奖 ("prize draw"), 6 are the same message reposted verbatim (马上开奖，祝您好运 with emoji), so the clearest example of lottery framing in this data is boilerplate rather than spontaneous usage.

Widening the lexicon with frequent expectation vocabulary (牛股 "bull stock", 黑马 "dark horse", 暴涨 "surge") raises the counts but matches ordinary business jargon, which reintroduces the same topic problem at a different set of terms.

The corpora themselves are unfavourable for the question. Board 600519 belongs to a stock held predominantly by long-term investors, and the title corpus predates current forum slang.

## Classifier

Weak supervision on the gambling tiers is not possible on this data: 4 positive documents. The module reports this instead of fitting a model.

Trained on the TRADING_MECHANICS tier (95 positives), the classifier reaches a 5-fold cross-validated ROC-AUC of 0.865 against the weak labels. Among documents with no seed term, the highest-scored are promotional: 要涨3倍 ("will triple"), 翻番利器 ("doubling weapon"), 井喷 ("gusher"), 暴涨. These are candidate terms for a future lexicon revision. The AUC is measured against lexicon-derived labels and does not indicate accuracy relative to human judgement.

## Index

`scripts/build_index.py` produces `data/pilot/daily_gdi.csv`: 361 daily observations (2015–2022) of marker densities for board 300343.

## Caveats

Small samples; two boards; different periods and genres (titles and replies); one blue chip and one small cap. The two corpora are not comparable to each other. The absence of gambling-tier vocabulary is a statement about these corpora and this seed lexicon and does not generalise to Chinese investors.
