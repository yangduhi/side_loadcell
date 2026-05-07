# AGENTS.md — NHTSA 측면 충돌 로드셀·차체 감가속도 분석 프로젝트

## 프로젝트 미션

NHTSA 측면 폴 충돌 시험 데이터를 활용하여 로드셀 배리어 force-time, 차체 감가속도, 차량 제원을 결합 분석한다. 최종 목표는 다음 산출물이다.

- 차체 부재/영역별 에너지 흡수량 추정
- 시간대별 하중 분포 및 하중 중심 이동
- 부재/영역별 하중 분담률
- 제조사·모델·차종·질량·연식별 구조 응답 특성 비교
- 재현 가능한 코호트, 데이터 계약, 품질 게이트, 리포트/대시보드

## 불변 기준

- 초기 분석 코호트는 CSV 후보 555건 중 `test_no=15452`를 제외한 554건이다.
- 기본 코호트 조건은 `crash_type_rule=side`, `test_config_code=VTP`, `test_config_label=VEHICLE INTO POLE`, `load_cell_barrier_family=side_pole_load_cell_barrier`, `load_cell_barrier_classification_id=side_pole_load_cell_8`이다.
- `test_no=15452`는 `ITV`, `IMPACTOR INTO VEHICLE`, `advanced_11x16_176_full`, `frontal_or_flat_load_cell_wall`이므로 기본 측면 폴 코호트에서 제외한다.
- SQLite의 `files`, `instrumentation_channels`, `injury_metrics`, `intrusions`가 0건이면 시계열 분석은 준비 미완료 상태로 판정한다.
- 원천 force-time 또는 acceleration-time 없이 peak force, impulse, ΔV, energy를 실제 산출한 것처럼 기술하지 않는다.
- 부재별 에너지 흡수량은 직접 관측값이 아니며 `engineering_estimate` 플래그와 근거 수준을 반드시 남긴다.

## 데이터 우선순위

| 목적 | 1차 소스 | 2차 소스 | 비고 |
|---|---|---|---|
| 초기 코호트 확정 | `side_loadcell_filtered_tests.csv` | SQLite `tests` | CSV가 문서 기준 코호트 소스 |
| 차량 제원 | CSV | SQLite `vehicles` | 결측/불일치 시 reconciliation 로그 필수 |
| 배리어 분류 | CSV | SQLite `tests`, `barriers` | side_pole_load_cell_8만 기본 코호트 |
| 시계열 파일 | NHTSA raw time-history | SQLite `files` | 현재 SQLite는 비어 있음 |
| 채널 정보 | raw file header | SQLite `instrumentation_channels` | 현재 SQLite는 비어 있음 |
| 사진/영상/리포트 | NHTSA assets | SQLite `files` | 부재 매핑 검증용 |

## 디렉터리 계약

```text
data/source/                 # 제공 CSV, SQLite
data/raw/time_history/        # NHTSA 원천 시계열 파일
data/raw/assets/              # 사진, 영상, PDF 리포트
data/processed/               # 코호트, 정규화 채널, 신호 전처리 결과
data/derived/                 # metrics, energy, benchmark tables
artifacts/harness/            # 검증 JSON, QA 로그, 회귀 비교 결과
reports/                      # Markdown, DOCX, dashboard export
.agents/                      # 역할 기반 에이전트 지침
.skills/                      # 반복 작업 절차
.harness/                     # 자동화·품질 게이트
```

## 작업 게이트

1. **G0 Metadata Baseline**: CSV/SQLite 구조·건수·코호트 재현 확인
2. **G1 Raw Asset Inventory**: raw 파일·사진·리포트 수집 상태 확인
3. **G2 Channel Dictionary**: 채널명·단위·축·센서 위치·샘플링 정의
4. **G3 Signal QA**: baseline correction, 단위 변환, filtering, time-zero 정렬, 결측/포화 점검
5. **G4 Metrics**: peak, time-to-peak, impulse, ΔV, relative displacement, load share 산출
6. **G5 Energy Mapping**: cell/zone/member energy와 근거 수준 산출
7. **G6 Benchmark & Reporting**: 제조사·모델 특성 비교와 보고서/대시보드 반영

## 에이전트 운영 규칙

- 에이전트는 `.agents/registry.yaml`의 순서대로 handoff한다.
- 각 에이전트는 자신의 산출물에 `source`, `assumption`, `qa_status`, `known_limitations`를 남긴다.
- 데이터가 없으면 추정하지 말고 blocked 상태를 기록한다.
- 단위가 불명확하면 수치 계산을 중단하고 channel dictionary 보완 태스크를 생성한다.
- 로드셀 cell-to-member 매핑은 사진/영상/리포트 또는 명시적 geometry table이 없으면 confidence를 `low`로 유지한다.
- 보고서에는 raw 시계열 미확보 상태와 engineering estimate 한계를 명시한다.

## 코드 스타일

- Python 3.11 이상 권장.
- I/O 경로는 CLI 인자로 받고, 저장소 절대경로를 하드코딩하지 않는다.
- 단위 변환, 필터, time-zero, drift correction은 함수 단위로 분리한다.
- 모든 metrics 테이블은 `test_no`, `run_id`, `metric_version`, `qa_status`를 포함한다.
- 스크립트는 실패 시 non-zero exit code를 반환한다.
