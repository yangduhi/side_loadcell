#!/usr/bin/env python3
"""Common utilities for the NHTSA side impact harness."""

from __future__ import annotations

import csv
import json
import math
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


REQUIRED_CSV_COLUMNS = [
    "test_no", "model_year", "make", "model", "body_style", "crash_type",
    "crash_type_rule", "test_config_code", "test_config_label", "impact_speed_value",
    "impact_speed_unit", "load_cell_barrier_family", "load_cell_barrier_classification_id",
    "load_cell_barrier_config_version", "test_weight_kg", "curb_weight_kg",
    "length_mm", "width_mm", "wheelbase_mm", "vax_crush_distance_mm",
]


COHORT_FILTERS = {
    "crash_type_rule": "side",
    "test_config_code": "VTP",
    "test_config_label": "VEHICLE INTO POLE",
    "load_cell_barrier_family": "side_pole_load_cell_barrier",
    "load_cell_barrier_classification_id": "side_pole_load_cell_8",
}


EXCLUDED_TEST_NOS = {"15452"}


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: str | Path) -> tuple[list[dict[str, str]], list[str]]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for row in reader]
        columns = list(reader.fieldnames or [])
    return rows, columns


def write_csv_rows(path: str | Path, rows: list[dict[str, Any]], columns: Optional[list[str]] = None) -> None:
    ensure_parent(path)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=False)


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def is_recommended_cohort_row(row: dict[str, str]) -> bool:
    test_no = str(row.get("test_no", "")).strip()
    if test_no in EXCLUDED_TEST_NOS:
        return False
    for key, expected in COHORT_FILTERS.items():
        if str(row.get(key, "")).strip() != expected:
            return False
    return True


def is_excluded_row(row: dict[str, str]) -> bool:
    return not is_recommended_cohort_row(row)


def to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None
    try:
        x = float(s)
    except ValueError:
        return None
    if math.isnan(x):
        return None
    return x


def top_counts(rows: Iterable[dict[str, str]], column: str, limit: int = 20) -> list[dict[str, Any]]:
    c = Counter(str(r.get(column, "")).strip() or "<missing>" for r in rows)
    return [{"value": value, "count": count} for value, count in c.most_common(limit)]


def numeric_summary(rows: Iterable[dict[str, str]], column: str) -> dict[str, Any]:
    xs = [to_float(r.get(column)) for r in rows]
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"count": 0, "missing": None}
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    def pct(p: float) -> float:
        if n == 1:
            return xs_sorted[0]
        idx = (n - 1) * p
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return xs_sorted[lo]
        return xs_sorted[lo] * (hi - idx) + xs_sorted[hi] * (idx - lo)
    return {
        "count": n,
        "min": xs_sorted[0],
        "p25": pct(0.25),
        "median": pct(0.50),
        "p75": pct(0.75),
        "max": xs_sorted[-1],
        "mean": sum(xs_sorted) / n,
    }


def sqlite_table_counts(sqlite_path: str | Path) -> dict[str, int]:
    p = Path(sqlite_path)
    if not p.exists():
        raise FileNotFoundError(f"SQLite DB not found: {p}")
    con = sqlite3.connect(str(p))
    try:
        cur = con.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        counts: dict[str, int] = {}
        for table in tables:
            counts[table] = int(cur.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
        return counts
    finally:
        con.close()


def sqlite_scalar(sqlite_path: str | Path, sql: str) -> Any:
    con = sqlite3.connect(str(sqlite_path))
    try:
        return con.execute(sql).fetchone()[0]
    finally:
        con.close()
