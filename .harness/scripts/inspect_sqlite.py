#!/usr/bin/env python3
"""Inspect SQLite tables and optionally run project SQL snippets."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sqlite", required=True)
    parser.add_argument("--sql", help="Optional SQL file to execute")
    args = parser.parse_args()

    con = sqlite3.connect(args.sqlite)
    con.row_factory = sqlite3.Row
    try:
        if args.sql:
            sql = Path(args.sql).read_text(encoding="utf-8")
            cur = con.execute(sql)
            rows = cur.fetchall()
            if rows:
                print("\t".join(rows[0].keys()))
                for row in rows:
                    print("\t".join(str(row[k]) for k in row.keys()))
            return 0

        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print("table\trow_count")
        for table in tables:
            count = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            print(f"{table}\t{count}")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
