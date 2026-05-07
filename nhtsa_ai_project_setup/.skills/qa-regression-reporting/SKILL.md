# Skill — QA, Regression & Reporting

## When to use

코드 변경, 데이터 변경, parser 변경, metrics 버전 변경, 보고서 작성 전 사용한다.

## Inputs

- `.harness/quality_gates.yaml`
- `.harness/scripts/*.py`
- `artifacts/harness/*.json`
- `data/derived/*.csv`

## Procedure

1. baseline validation 실행
2. cohort build 재실행
3. metadata profile 재생성
4. metrics schema validation 실행
5. 이전 metric run과 비교
6. readiness/report artifact 생성
7. QA 통과 결과만 보고서에 반영

## Commands

```bash
make -f .harness/Makefile all
python .harness/scripts/validate_signal_metrics.py --loadcell data/derived/loadcell_metrics.csv --vehicle data/derived/vehicle_deceleration_metrics.csv --out artifacts/harness/metrics_schema_validation.json
```

## Outputs

- `artifacts/harness/*_validation.json`
- `reports/project_readiness_report.md`
- `reports/side_impact_analysis_report.md`
