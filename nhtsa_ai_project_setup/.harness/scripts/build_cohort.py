#!/usr/bin/env python3
"""Build the recommended 554-test side-pole VTP cohort and explicit exclusions."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from common import (
    COHORT_FILTERS,
    EXCLUDED_TEST_NOS,
    is_recommended_cohort_row,
    read_csv_rows,
    top_counts,
    write_csv_rows,
    write_json,
)


def exclusion_reason(row: dict[str, str]) -> str:
    test_no = str(row.get("test_no", "")).strip()
    if test_no in EXCLUDED_TEST_NOS:
        return "Explicit hard exclusion: non-VTP side pole cohort member"
    mismatches = []
    for key, expected in COHORT_FILTERS.items():
        observed = str(row.get(key, "")).strip()
        if observed != expected:
            mismatches.append(f"{key}={observed!r} != {expected!r}")
    return "; ".join(mismatches) or "Not in recommended cohort"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--exclusions", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    rows, columns = read_csv_rows(args.csv)
    cohort = [r for r in rows if is_recommended_cohort_row(r)]
    exclusions = []
    for row in rows:
        if not is_recommended_cohort_row(row):
            r = dict(row)
            r["exclusion_reason"] = exclusion_reason(row)
            exclusions.append(r)

    write_csv_rows(args.out, cohort, columns)
    write_csv_rows(args.exclusions, exclusions, columns + ["exclusion_reason"])

    summary = {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_csv": args.csv,
        "cohort_csv": args.out,
        "exclusions_csv": args.exclusions,
        "source_rows": len(rows),
        "recommended_cohort_rows": len(cohort),
        "excluded_rows": len(exclusions),
        "expected_recommended_cohort_rows": 554,
        "status": "pass" if len(cohort) == 554 and len(exclusions) == 1 else "fail",
        "filters": COHORT_FILTERS,
        "hard_excluded_test_no": sorted(EXCLUDED_TEST_NOS),
        "top_makes": top_counts(cohort, "make", limit=12),
        "top_body_styles": top_counts(cohort, "body_style", limit=12),
        "model_year_distribution": top_counts(cohort, "model_year", limit=40),
    }
    write_json(args.summary, summary)
    print(f"cohort rows={len(cohort)} exclusions={len(exclusions)} status={summary['status']}")
    return 0 if summary["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
