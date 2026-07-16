"""Daily Gambling Discourse Index: gambling hits per 100 tokens per day."""
import csv, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from gambling_nlp import score_text

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "pilot", "user_comments.csv")
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "pilot", "daily_gdi.csv")

by_day = defaultdict(lambda: {"docs": 0, "tokens": 0, "gamb": 0, "restr": 0})
seen = set()
with open(DATA, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        text = (r.get("reply_text") or "").strip()
        day = (r.get("reply_publish_time") or "")[:10]
        if not text or not day or (day, text) in seen:
            continue
        seen.add((day, text))
        res = score_text(text)
        d = by_day[day]
        d["docs"] += 1; d["tokens"] += res.n_tokens
        d["gamb"] += res.gambling_hits; d["restr"] += res.restraint_hits

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["date", "docs", "tokens", "gambling_hits", "restraint_hits", "gdi"])
    for day in sorted(by_day):
        d = by_day[day]
        gdi = 100 * d["gamb"] / d["tokens"] if d["tokens"] else 0.0
        w.writerow([day, d["docs"], d["tokens"], d["gamb"], d["restr"], f"{gdi:.3f}"])

print(f"wrote {OUT} ({len(by_day)} days)")
with open(OUT, encoding="utf-8") as f:
    for line in f.read().splitlines()[:8]:
        print(" ", line)
