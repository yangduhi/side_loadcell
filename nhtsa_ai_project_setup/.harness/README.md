# .harness

NHTSA 측면 충돌 분석 프로젝트의 데이터 계약·코호트 재현·품질 게이트·회귀 검증 자동화 디렉터리입니다.

## 주요 구성

| 파일/디렉터리 | 역할 |
|---|---|
| `config.yaml` | 경로, 코호트, 신호처리, 산출물 기본 설정 |
| `cohort_rules.yaml` | 554건 권장 코호트 재현 조건 |
| `data_contract.yaml` | CSV/SQLite/향후 metrics 테이블 schema 계약 |
| `quality_gates.yaml` | G0~G6 품질 게이트 |
| `pipeline.yaml` | 전체 실행 순서와 산출물 연결 |
| `scripts/` | 실제 실행 스크립트 |
| `sql/` | SQLite 감사 쿼리 |
| `tests/` | pytest 기반 smoke/regression tests |
| `templates/` | raw inventory, channel dictionary, mapping template |

## 1차 실행 순서

```bash
python .harness/scripts/validate_baseline.py --csv data/source/side_loadcell_filtered_tests.csv --sqlite data/source/nhtsa_gui.sqlite --out artifacts/harness/baseline_validation.json
python .harness/scripts/build_cohort.py --csv data/source/side_loadcell_filtered_tests.csv --out data/processed/side_pole_vtp_cohort.csv --exclusions data/processed/excluded_tests.csv --summary artifacts/harness/cohort_summary.json
python .harness/scripts/profile_metadata.py --cohort data/processed/side_pole_vtp_cohort.csv --out artifacts/harness/metadata_profile.json
python .harness/scripts/make_readiness_report.py --baseline artifacts/harness/baseline_validation.json --cohort artifacts/harness/cohort_summary.json --profile artifacts/harness/metadata_profile.json --out reports/project_readiness_report.md
```

## 판정 해석

- `pass`: 다음 단계 진행 가능
- `pass_with_known_blockers`: 메타데이터 기준은 통과했지만 raw 시계열 등 후속 필수 데이터가 없음
- `blocked`: 선행 데이터 또는 계약 위반으로 다음 단계 진행 불가
- `fail`: 데이터 불일치 또는 스크립트 오류
