# NHTSA 측면 충돌 분석 프로젝트 AI 작업 세팅

이 패키지는 `NHTSA 시험데이터 기반 측면 충돌 로드셀·차체 감가속도 분석 프로젝트 개요 및 기획서`에 맞춘 선행 세팅입니다. 목적은 다음 세 가지입니다.

1. `.agents` — 프로젝트에 투입할 역할 기반 AI/개발 에이전트 운영 규칙 정의
2. `.skills` — 반복 가능한 분석·검증 절차를 스킬 단위로 표준화
3. `.harness` — 데이터 계약, 코호트 재현, 품질 게이트, 회귀 검증을 자동화

## 권장 적용 위치

저장소 루트 예시:

```text
D:/vscode/nhtsa_metadata_deformation/
├─ AGENTS.md
├─ .agents/
├─ .skills/
├─ .harness/
├─ data/
│  ├─ source/
│  │  ├─ side_loadcell_filtered_tests.csv
│  │  └─ nhtsa_gui.sqlite
│  ├─ raw/time_history/
│  ├─ processed/
│  └─ derived/
├─ docs/
│  └─ NHTSA_side_impact_project_plan.docx
└─ reports/
```

현재 제공 데이터 기준 핵심 전제는 다음과 같습니다.

| 항목 | 기준값 |
|---|---:|
| CSV 후보 건수 | 555 |
| 권장 분석 코호트 | 554 |
| 제외 시험번호 | 15452 |
| 기본 코호트 조건 | `VTP` + `VEHICLE INTO POLE` + `side_pole_load_cell_8` |
| SQLite `files` | 0 |
| SQLite `instrumentation_channels` | 0 |

## 빠른 실행

Windows PowerShell 기준:

```powershell
python .harness/scripts/validate_baseline.py `
  --csv data/source/side_loadcell_filtered_tests.csv `
  --sqlite data/source/nhtsa_gui.sqlite `
  --out artifacts/harness/baseline_validation.json

python .harness/scripts/build_cohort.py `
  --csv data/source/side_loadcell_filtered_tests.csv `
  --out data/processed/side_pole_vtp_cohort.csv `
  --exclusions data/processed/excluded_tests.csv `
  --summary artifacts/harness/cohort_summary.json

python .harness/scripts/profile_metadata.py `
  --cohort data/processed/side_pole_vtp_cohort.csv `
  --out artifacts/harness/metadata_profile.json

python .harness/scripts/make_readiness_report.py `
  --baseline artifacts/harness/baseline_validation.json `
  --cohort artifacts/harness/cohort_summary.json `
  --profile artifacts/harness/metadata_profile.json `
  --out reports/project_readiness_report.md
```

Bash 기준:

```bash
make -f .harness/Makefile validate CSV=data/source/side_loadcell_filtered_tests.csv SQLITE=data/source/nhtsa_gui.sqlite
make -f .harness/Makefile cohort CSV=data/source/side_loadcell_filtered_tests.csv
make -f .harness/Makefile profile
make -f .harness/Makefile readiness
```

## 운영 원칙

- CSV `side_loadcell_filtered_tests.csv`는 초기 권장 코호트의 기준 소스입니다.
- SQLite는 시험·차량·배리어 메타데이터 보강용입니다.
- 현재 SQLite의 시계열/파일 테이블이 비어 있으므로 force-time, acceleration-time, 에너지 산출은 raw time-history 확보 후에만 수행합니다.
- “부재별 에너지 흡수량”은 직접 계측값이 아니라 로드셀 위치·접촉시간·차체 제원·crush·감가속도 기반 상대변위·사진/영상 검증을 결합한 engineering estimate로 관리합니다.
- 모든 산출물은 `.harness/quality_gates.yaml`의 게이트를 통과해야 보고서 또는 대시보드에 반영합니다.
