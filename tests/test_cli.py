import csv
import io
import os
from contextlib import redirect_stdout

from gambling_nlp.cli import main


def test_cli_scores_demo_csv():
    demo_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "demo_posts.csv"
    )
    out = io.StringIO()
    with redirect_stdout(out):
        main([demo_path])

    rows = list(csv.DictReader(io.StringIO(out.getvalue())))
    assert len(rows) == 6
    assert rows[0]["gambling_hits"] != "0"
    assert rows[2]["restraint_hits"] != "0"
    assert float(rows[5]["gambling_hits"]) == 0.0
    assert "matched_terms" in rows[0]
