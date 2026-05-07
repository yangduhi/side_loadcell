#!/usr/bin/env python3
"""Validate the current CSV/SQLite baseline against the project plan.

This script is intentionally strict about the filtered CSV cohort and explicit
about the known time-history blocker in SQLite.
"""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from common import (
    COHORT_FILTERS,
    EXCLUDED_TEST_NOS,
    REQUIRED_CSV_COLUMNS,
    is_recommended_cohort_row,
    read_csv_rows,
    sqlite_table_counts,
    write_json,
)


REQUIRED_SQLITE_TABLES = [
    "tests", "vehicles", "barriers", "files", "instrumentation_channels",
    "injury_metrics", "intrusions", "occupants", "restraints", "source_payloads",
]


def sqlite_count(sqlite_path: Path, sql: str) -> int:
    con = sqlite3.connect(str(sqlite_path))
    try:
        return int(con.execute(sql).fetchone()[0])
    finally:
        con.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to side_loadcell_filtered_tests.csv")
    parser.add_argument("--sqlite", required=True, help="Path to nhtsa_gui.sqlite")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    sqlite_path = Path(args.sqlite)

    checks = []
    warnings = []
    blockers = []

    rows, columns = read_csv_rows(csv_path)
    missing_cols = [c for c in REQUIRED_CSV_COLUMNS if c not in columns]
    checks.append({
        "id": "csv_required_columns",
        "status": "pass" if not missing_cols else "fail",
        "observed_columns": columns,
        "missing_columns": missing_cols,
    })

    source_row_count = len(rows)
    checks.append({
        "id": "csv_source_row_count",
        "expected": 555,
        "observed": source_row_count,
        "status": "pass" if source_row_count == 555 else "fail",
    })

    test_nos = [str(r.get("test_no", "")).strip() for r in rows]
    unique_test_no_count = len(set(test_nos))
    checks.append({
        "id": "csv_unique_test_no",
        "expected": source_row_count,
        "observed": unique_test_no_count,
        "status": "pass" if unique_test_no_count == source_row_count else "fail",
    })

    excluded_present = sorted(EXCLUDED_TEST_NOS.intersection(test_nos))
    checks.append({
        "id": "excluded_test_no_present",
        "expected": sorted(EXCLUDED_TEST_NOS),
        "observed": excluded_present,
        "status": "pass" if set(excluded_present) == EXCLUDED_TEST_NOS else "fail",
    })

    cohort_rows = [r for r in rows if is_recommended_cohort_row(r)]
    checks.append({
        "id": "recommended_cohort_count",
        "expected": 554,
        "observed": len(cohort_rows),
        "filters": COHORT_FILTERS,
        "excluded_test_no": sorted(EXCLUDED_TEST_NOS),
        "status": "pass" if len(cohort_rows) == 554 else "fail",
    })

    table_counts = sqlite_table_counts(sqlite_path)
    missing_tables = [t for t in REQUIRED_SQLITE_TABLES if t not in table_counts]
    checks.append({
        "id": "sqlite_required_tables",
        "status": "pass" if not missing_tables else "fail",
        "missing_tables": missing_tables,
        "table_counts": table_counts,
    })

    files_count = int(table_counts.get("files", -1))
    channel_count = int(table_counts.get("instrumentation_channels", -1))
    injury_count = int(table_counts.get("injury_metrics", -1))
    intrusions_count = int(table_counts.get("intrusions", -1))

    if files_count == 0:
        blockers.append("SQLite files table has 0 rows; raw asset inventory is not loaded.")
    if channel_count == 0:
        blockers.append("SQLite instrumentation_channels table has 0 rows; channel-level time-history metadata is not loaded.")
    if injury_count == 0:
        warnings.append("SQLite injury_metrics table has 0 rows; occupant injury metrics are outside current baseline.")
    if intrusions_count == 0:
        warnings.append("SQLite intrusions table has 0 rows; intrusion validation is outside current baseline.")

    if "tests" in table_counts:
        sqlite_side_pole_count = sqlite_count(
            sqlite_path,
            """
            SELECT COUNT(*) FROM tests
            WHERE test_config_code='VTP'
              AND load_cell_barrier_family='side_pole_load_cell_barrier'
              AND load_cell_barrier_classification_id='side_pole_load_cell_8'
            """,
        )
        checks.append({
            "id": "sqlite_broader_side_pole_inventory",
            "observed": sqlite_side_pole_count,
            "status": "warn" if sqlite_side_pole_count != len(cohort_rows) else "pass",
            "note": "SQLite may contain broader inventory than the filtered CSV. CSV remains initial cohort authority.",
        })
        if sqlite_side_pole_count != len(cohort_rows):
            warnings.append(
                f"SQLite VTP side_pole_load_cell_8 inventory count is {sqlite_side_pole_count}, "
                f"while filtered CSV recommended cohort is {len(cohort_rows)}. Reconcile only if project scope changes."
            )

    hard_fail = any(c.get("status") == "fail" for c in checks)
    if hard_fail:
        status = "fail"
    elif blockers:
        status = "pass_with_known_blockers"
    else:
        status = "pass"

    payload = {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "csv_path": str(csv_path),
        "sqlite_path": str(sqlite_path),
        "checks": checks,
        "warnings": warnings,
        "blockers": blockers,
        "next_gate": "G1_raw_asset_inventory" if status != "fail" else "G0_metadata_baseline_rework",
    }
    write_json(args.out, payload)
    print(f"baseline status={status}; output={args.out}")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
