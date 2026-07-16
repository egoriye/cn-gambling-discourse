"""Command-line interface.

Usage:
    python -m gambling_nlp.cli data/demo_posts.csv --text-column text

Input: a CSV file with one document per row.
Output: the same table with gambling/restraint scores appended, printed
to stdout as CSV (redirect to a file to save).
"""

from __future__ import annotations

import argparse
import csv
import sys

from .scoring import score_text


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Score Chinese texts for gambling-discourse markers."
    )
    parser.add_argument("csv_path", help="Input CSV file")
    parser.add_argument("--text-column", default="text",
                        help="Name of the column containing the text")
    args = parser.parse_args(argv)

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or args.text_column not in reader.fieldnames:
            sys.exit(f"Column '{args.text_column}' not found in {args.csv_path}")
        out_fields = list(reader.fieldnames) + [
            "n_tokens", "gambling_hits", "restraint_hits",
            "gambling_score", "restraint_score", "net_score", "matched_terms",
        ]
        writer = csv.DictWriter(sys.stdout, fieldnames=out_fields)
        writer.writeheader()
        for row in reader:
            res = score_text(row[args.text_column])
            row.update({
                "n_tokens": res.n_tokens,
                "gambling_hits": res.gambling_hits,
                "restraint_hits": res.restraint_hits,
                "gambling_score": f"{res.gambling_score:.2f}",
                "restraint_score": f"{res.restraint_score:.2f}",
                "net_score": f"{res.net_score:.2f}",
                "matched_terms": " ".join(sorted(res.hits)),
            })
            writer.writerow(row)


if __name__ == "__main__":
    main()
