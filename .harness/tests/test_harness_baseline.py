"""Pytest smoke tests for the NHTSA side-impact harness.

Run from repository root after placing source data in data/source/:
  pytest .harness/tests
"""

from pathlib import Path
import subprocess
import sys
import json


ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data/source/side_loadcell_filtered_tests.csv"
SQLITE = ROOT / "data/source/nhtsa_gui.sqlite"


def test_validate_baseline_script_exists():
    assert (ROOT / ".harness/scripts/validate_baseline.py").exists()


def test_baseline_validation_runs_when_source_data_exists(tmp_path):
    if not CSV.exists() or not SQLITE.exists():
        return
    out = tmp_path / "baseline.json"
    cmd = [
        sys.executable,
        str(ROOT / ".harness/scripts/validate_baseline.py"),
        "--csv", str(CSV),
        "--sqlite", str(SQLITE),
        "--out", str(out),
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr + result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["status"] in {"pass", "pass_with_known_blockers"}


def test_build_cohort_runs_when_source_data_exists(tmp_path):
    if not CSV.exists():
        return
    out = tmp_path / "cohort.csv"
    excl = tmp_path / "excluded.csv"
    summary = tmp_path / "summary.json"
    cmd = [
        sys.executable,
        str(ROOT / ".harness/scripts/build_cohort.py"),
        "--csv", str(CSV),
        "--out", str(out),
        "--exclusions", str(excl),
        "--summary", str(summary),
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr + result.stdout
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["recommended_cohort_rows"] == 554
    assert payload["excluded_rows"] == 1
