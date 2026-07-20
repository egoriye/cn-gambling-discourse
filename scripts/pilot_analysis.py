"""Pilot: score two public Guba sample corpora (IVTz/GubaScraper).

Reports the gambling tier and the trading-mechanics tier separately, since
the point of the exercise is that they behave very differently.

Run: python scripts/pilot_analysis.py  (downloads data on first run)
"""

from __future__ import annotations

import csv
import json
import os
import sys
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from gambling_nlp import score_text  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pilot")
URLS = {
    "comments.json": (
        "https://raw.githubusercontent.com/IVTz/GubaScraper/main/"
        "json%E6%A0%BC%E5%BC%8F%E8%AF%84%E8%AE%BA%E7%A4%BA%E4%BE%8B.json"
    ),
    "user_comments.csv": (
        "https://raw.githubusercontent.com/IVTz/GubaScraper/main/"
        "%E7%94%A8%E6%88%B7%E5%B1%82%E9%9D%A2%E8%AF%84%E8%AE%BA"
        "%E6%95%B0%E6%8D%AE%E7%A4%BA%E4%BE%8B.csv"
    ),
}


def ensure_data() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    for fname, url in URLS.items():
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            print(f"downloading {fname} ...", file=sys.stderr)
            urllib.request.urlretrieve(url, path)


def load_corpora() -> dict[str, list[str]]:
    with open(os.path.join(DATA_DIR, "comments.json"), encoding="utf-8") as f:
        posts = json.load(f)
    titles = [p["post_title"] for p in posts if p.get("post_title")]
    with open(os.path.join(DATA_DIR, "user_comments.csv"),
              encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    replies = [r["reply_text"] for r in rows if r.get("reply_text", "").strip()]
    # drop exact duplicates (reposted spam)
    return {
        "titles_600519_2001_2012": sorted(set(titles)),
        "replies_300343_2015_2022": sorted(set(replies)),
    }


def analyze(name: str, docs: list[str]) -> None:
    res = [score_text(d) for d in docs]
    n = len(res)
    tokens = sum(r.n_tokens for r in res)
    terms: Counter = Counter()
    for r in res:
        terms.update(r.hits)

    def tier(label: str, doc_pred, hit_sum: int) -> None:
        d = sum(1 for r in res if doc_pred(r))
        print(f"  {label:<22} {d:>4} docs ({100*d/n:>4.1f}%)  "
              f"{hit_sum:>3} hits  density {100*hit_sum/tokens:.3f}")

    print(f"\n## {name}: {n} docs, {tokens} tokens")
    tier("gambling (marked)", lambda r: r.gambling_hits > 0,
         sum(r.gambling_hits for r in res))
    tier("trading mechanics", lambda r: r.mechanics_hits > 0,
         sum(r.mechanics_hits for r in res))
    tier("restraint", lambda r: r.restraint_hits > 0,
         sum(r.restraint_hits for r in res))
    print(f"  top terms: {terms.most_common(8)}")


def main() -> None:
    ensure_data()
    for name, docs in load_corpora().items():
        analyze(name, docs)


if __name__ == "__main__":
    main()
