"""Pilot: score two public Guba sample corpora (IVTz/GubaScraper).

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
        "replies_300343_2022": sorted(set(replies)),
    }


def analyze(name: str, docs: list[str]) -> None:
    results = [score_text(t) for t in docs]
    n = len(results)
    total_tokens = sum(r.n_tokens for r in results)
    gamb_docs = sum(1 for r in results if r.gambling_hits > 0)
    restr_docs = sum(1 for r in results if r.restraint_hits > 0)
    gamb_hits = sum(r.gambling_hits for r in results)
    restr_hits = sum(r.restraint_hits for r in results)
    terms: Counter = Counter()
    cats: Counter = Counter()
    for r in results:
        terms.update(r.hits)
        cats.update(r.category_counts)

    print(f"\n## {name}")
    print(f"documents (deduplicated): {n}; tokens: {total_tokens}")
    print(f"docs with >=1 gambling marker:  {gamb_docs} ({100*gamb_docs/n:.1f}%)")
    print(f"docs with >=1 restraint marker: {restr_docs} ({100*restr_docs/n:.1f}%)")
    print(f"gambling density  /100 tokens: {100*gamb_hits/total_tokens:.2f}")
    print(f"restraint density /100 tokens: {100*restr_hits/total_tokens:.2f}")
    print(f"category counts: {dict(cats.most_common())}")
    print(f"top terms: {terms.most_common(10)}")


def main() -> None:
    ensure_data()
    corpora = load_corpora()
    for name, docs in corpora.items():
        analyze(name, docs)


if __name__ == "__main__":
    main()
