# Agent 01 — Data Contract & Cohort Auditor

## 미션

제공 CSV와 SQLite의 구조, 건수, 필수 컬럼, 코호트 재현성을 검증한다. 문서의 핵심 수치가 현재 데이터와 일치하는지 자동화된 재현 결과로 남긴다.

## 필수 검증

- CSV 건수: 555
- CSV 필수 컬럼 20개 존재
- `test_no` 유일성
- `test_no=15452` 존재 및 제외 사유 기록
- 기본 코호트 554건 재현
- SQLite 주요 테이블 존재 및 row count 기록
- `files=0`, `instrumentation_channels=0`이면 time-history 미확보 blocker 등록
- SQLite 전체 side-pole 후보와 CSV filtered cohort 간 범위 차이를 warning으로 기록

## 실행 명령

```bash
python .harness/scripts/validate_baseline.py \
  --csv data/source/side_loadcell_filtered_tests.csv \
  --sqlite data/source/nhtsa_gui.sqlite \
  --out artifacts/harness/baseline_validation.json
```

```bash
python .harness/scripts/build_cohort.py \
  --csv data/source/side_loadcell_filtered_tests.csv \
  --out data/processed/side_pole_vtp_cohort.csv \
  --exclusions data/processed/excluded_tests.csv \
  --summary artifacts/harness/cohort_summary.json
```

## 산출물

- `artifacts/harness/baseline_validation.json`
- `data/processed/side_pole_vtp_cohort.csv`
- `data/processed/excluded_tests.csv`
- `artifacts/harness/cohort_summary.json`

## 완료 조건

G0 Metadata Baseline이 `pass` 또는 `pass_with_known_blockers` 상태여야 한다. 현재 계획상 `files=0`, `instrumentation_channels=0`은 분석 blocker지만 메타데이터 baseline 실패는 아니다.
