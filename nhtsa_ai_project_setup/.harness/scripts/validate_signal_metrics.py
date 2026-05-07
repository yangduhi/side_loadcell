#!/usr/bin/env python3
"""Validate future signal metric CSV schemas before reporting."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from common import read_csv_rows, write_json


LOADCELL_REQUIRED = [
    "test_no", "run_id", "metric_version", "channel_code", "cell_id",
    "peak_force_n", "time_to_peak_ms", "impulse_n_s", "force_duration_ms",
    "filter_applied", "qa_status", "qa_notes",
]

VEHICLE_REQUIRED = [
    "test_no", "run_id", "metric_version", "channel_code", "sensor_location_code", "axis",
    "peak_accel_mps2", "delta_v_mps", "relative_displacement_m",
    "drift_correction_method", "filter_applied", "qa_status", "qa_notes",
]


def validate_csv(path: str, required: list[str]) -> dict:
    p = Path(path)
    if not p.exists():
        return {"path": path, "status": "blocked", "reason": "file_not_found"}
    rows, cols = read_csv_rows(p)
    missing = [c for c in required if c not in cols]
    missing_qa = sum(1 for r in rows if not str(r.get("qa_status", "")).strip()) if "qa_status" in cols else len(rows)
    return {
        "path": path,
        "row_count": len(rows),
        "columns": cols,
        "missing_columns": missing,
        "missing_qa_status_rows": missing_qa,
        "status": "pass" if not missing and missing_qa == 0 else "fail",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loadcell", required=True)
    parser.add_argument("--vehicle", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    loadcell = validate_csv(args.loadcell, LOADCELL_REQUIRED)
    vehicle = validate_csv(args.vehicle, VEHICLE_REQUIRED)
    statuses = [loadcell["status"], vehicle["status"]]
    overall = "pass" if statuses == ["pass", "pass"] else "blocked" if "blocked" in statuses else "fail"
    payload = {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": overall,
        "loadcell_metrics": loadcell,
        "vehicle_deceleration_metrics": vehicle,
    }
    write_json(args.out, payload)
    print(f"metrics schema status={overall}; output={args.out}")
    return 0 if overall == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
