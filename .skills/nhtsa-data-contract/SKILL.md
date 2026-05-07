# Skill — NHTSA Data Contract & Cohort Reproduction

## When to use

프로젝트 착수, 데이터 변경, CSV/SQLite 교체, 코호트 재산출 전후에 사용한다.

## Inputs

- `data/source/side_loadcell_filtered_tests.csv`
- `data/source/nhtsa_gui.sqlite`
- `.harness/cohort_rules.yaml`

## Procedure

1. CSV 필수 컬럼 20개 확인
2. CSV row count 555 확인
3. `test_no` uniqueness 확인
4. `test_no=15452` 존재와 제외 사유 확인
5. VTP + side_pole_load_cell_8 조건으로 554건 코호트 산출
6. SQLite 주요 테이블 존재와 row count 확인
7. `files=0`, `instrumentation_channels=0`이면 raw 시계열 blocker 등록
8. SQLite broader inventory와 CSV filtered cohort 불일치를 warning으로 기록

## Commands

```bash
python .harness/scripts/validate_baseline.py --csv data/source/side_loadcell_filtered_tests.csv --sqlite data/source/nhtsa_gui.sqlite --out artifacts/harness/baseline_validation.json
python .harness/scripts/build_cohort.py --csv data/source/side_loadcell_filtered_tests.csv --out data/processed/side_pole_vtp_cohort.csv --exclusions data/processed/excluded_tests.csv --summary artifacts/harness/cohort_summary.json
```

## Outputs

- `artifacts/harness/baseline_validation.json`
- `data/processed/side_pole_vtp_cohort.csv`
- `data/processed/excluded_tests.csv`

## Quality gate

G0 Metadata Baseline.
