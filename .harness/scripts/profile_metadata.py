#!/usr/bin/env python3
"""Profile the recommended cohort metadata for planning and QA."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from common import numeric_summary, read_csv_rows, top_counts, write_json


NUMERIC_COLUMNS = [
    "model_year", "impact_speed_value", "test_weight_kg", "curb_weight_kg",
    "length_mm", "width_mm", "wheelbase_mm", "vax_crush_distance_mm",
]


CATEGORICAL_COLUMNS = [
    "make", "model", "body_style", "crash_type", "test_config_code",
    "test_config_label", "load_cell_barrier_family", "load_cell_barrier_classification_id",
    "impact_speed_unit",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows, columns = read_csv_rows(args.cohort)
    missing_by_column = {
        c: sum(1 for r in rows if str(r.get(c, "")).strip() == "" or str(r.get(c, "")).strip().lower() == "nan")
        for c in columns
    }
    profile = {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_path": args.cohort,
        "row_count": len(rows),
        "columns": columns,
        "missing_by_column": missing_by_column,
        "numeric_summary": {c: numeric_summary(rows, c) for c in NUMERIC_COLUMNS if c in columns},
        "categorical_top_counts": {c: top_counts(rows, c, limit=20) for c in CATEGORICAL_COLUMNS if c in columns},
    }
    write_json(args.out, profile)
    print(f"profile rows={len(rows)} output={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
