#!/usr/bin/env python3
"""Create a Markdown readiness report from harness JSON artifacts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from common import ensure_parent, load_json


def fmt_check_table(checks):
    lines = ["| Check | Status | Expected | Observed |", "|---|---:|---:|---:|"]
    for c in checks:
        lines.append(
            f"| {c.get('id','')} | {c.get('status','')} | {c.get('expected','')} | {c.get('observed','')} |"
        )
    return "\n".join(lines)


def fmt_top(items, limit=12):
    if not items:
        return "없음"
    return ", ".join(f"{x.get('value')}({x.get('count')})" for x in items[:limit])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--cohort", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    baseline = load_json(args.baseline)
    cohort = load_json(args.cohort)
    profile = load_json(args.profile)

    blockers = baseline.get("blockers", [])
    warnings = baseline.get("warnings", [])

    text = f"""
# NHTSA 측면 충돌 분석 프로젝트 Readiness Report

- 생성 시각(UTC): {datetime.now(timezone.utc).isoformat()}
- Baseline status: `{baseline.get('status')}`
- Cohort status: `{cohort.get('status')}`
- 다음 게이트: `{baseline.get('next_gate')}`

## 1. 코호트 요약

| 항목 | 값 |
|---|---:|
| CSV 원천 건수 | {cohort.get('source_rows')} |
| 권장 분석 코호트 | {cohort.get('recommended_cohort_rows')} |
| 제외 건수 | {cohort.get('excluded_rows')} |
| 기대 코호트 건수 | {cohort.get('expected_recommended_cohort_rows')} |

기본 코호트 필터:

```text
{cohort.get('filters')}
```

하드 제외 시험번호: `{cohort.get('hard_excluded_test_no')}`

## 2. Baseline 검증 결과

{fmt_check_table(baseline.get('checks', []))}

## 3. Known Blockers

{chr(10).join('- ' + b for b in blockers) if blockers else '- 없음'}

## 4. Warnings

{chr(10).join('- ' + w for w in warnings) if warnings else '- 없음'}

## 5. 메타데이터 분포 요약

- 상위 제조사: {fmt_top(cohort.get('top_makes', []))}
- 상위 body style: {fmt_top(cohort.get('top_body_styles', []))}
- impact speed 요약: `{profile.get('numeric_summary', {}).get('impact_speed_value', {})}`
- test weight 요약: `{profile.get('numeric_summary', {}).get('test_weight_kg', {})}`
- width 요약: `{profile.get('numeric_summary', {}).get('width_mm', {})}`
- crush 요약: `{profile.get('numeric_summary', {}).get('vax_crush_distance_mm', {})}`

## 6. 다음 작업

1. `data/processed/raw_asset_inventory.csv` 생성
2. 시험번호별 raw time-history 파일 확보
3. 로드셀 force channel과 차체 acceleration channel dictionary 작성
4. 단위·축·샘플링·time-zero 검증 후 signal metrics 산출
5. cell/zone/member mapping table 작성 및 engineering estimate confidence 부여

## 7. 보고서 반영 시 주의 문구

현재 SQLite에는 시계열 및 파일 관련 테이블이 비어 있으므로 실제 force-time, acceleration-time, impulse, ΔV, 부재별 energy는 raw time-history 확보 전까지 산출 완료로 표현하면 안 됩니다. 부재별 에너지 흡수량은 직접 계측값이 아니라 engineering estimate입니다.
""".strip() + "\n"

    ensure_parent(args.out)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"readiness report written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
