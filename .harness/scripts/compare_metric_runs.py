#!/usr/bin/env python3
"""Compare two metric CSV runs by key and numeric columns.

Intended for regression checks after pipeline or parser changes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from common import read_csv_rows, to_float, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", required=True)
    parser.add_argument("--new", required=True)
    parser.add_argument("--keys", default="test_no,channel_code", help="Comma-separated key columns")
    parser.add_argument("--numeric", required=True, help="Comma-separated numeric columns to compare")
    parser.add_argument("--tolerance", type=float, default=1e-6)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    keys = [x.strip() for x in args.keys.split(",") if x.strip()]
    numeric = [x.strip() for x in args.numeric.split(",") if x.strip()]
    old_rows, _ = read_csv_rows(args.old)
    new_rows, _ = read_csv_rows(args.new)

    def index(rows):
        return {tuple(str(r.get(k, "")).strip() for k in keys): r for r in rows}

    old_i = index(old_rows)
    new_i = index(new_rows)
    missing_in_new = sorted([k for k in old_i if k not in new_i])
    added_in_new = sorted([k for k in new_i if k not in old_i])
    changed = []
    for k in sorted(set(old_i).intersection(new_i)):
        for col in numeric:
            a = to_float(old_i[k].get(col))
            b = to_float(new_i[k].get(col))
            if a is None or b is None:
                if a != b:
                    changed.append({"key": k, "column": col, "old": a, "new": b, "delta": None})
                continue
            delta = b - a
            if abs(delta) > args.tolerance:
                changed.append({"key": k, "column": col, "old": a, "new": b, "delta": delta})

    status = "pass" if not missing_in_new and not added_in_new and not changed else "fail"
    write_json(args.out, {
        "schema_version": "0.1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "keys": keys,
        "numeric_columns": numeric,
        "tolerance": args.tolerance,
        "old_row_count": len(old_rows),
        "new_row_count": len(new_rows),
        "missing_in_new": missing_in_new[:100],
        "added_in_new": added_in_new[:100],
        "changed_count": len(changed),
        "changed_sample": changed[:100],
    })
    print(f"compare status={status}; changed={len(changed)} output={args.out}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
