# Project Instructions

항상 한국어로 답변한다. 영어 요청이 있으면 그 언어로 전환한다.

## Project Mission

NHTSA 측면 폴 충돌 시험 데이터를 활용하여 로드셀 배리어 force-time, 차체 감가속도,
차량 제원을 결합 분석한다. 최종 산출물은 하중 분포, 하중 중심 이동, 부재/영역별
하중 분담률, engineering-estimate 기반 에너지 흡수량, 제조사/모델별 구조 응답 비교다.

## Scope

이 프로젝트는 `side_loadcell_filtered_tests.csv` 기준의 554건 side-pole load-cell 분석 준비 작업을 다룬다.

- 권위 있는 분석 scope: `data/side_loadcell_filtered_tests.csv`
- 최종 side-pole 분석 대상: 554건
- 제외된 filtered row: `15452`
- 제외된 연구용 availability rows: 34건 `research_other`
- waveform은 아직 파싱하지 않는다.
- waveform 연결 key는 `test_no + curve_no`다.
- 채널명은 공식 waveform 내부명이 아니라 metadata-derived channel name이다.

## Analysis-Ready DB

기본 산출물은 `data/side_pole_analysis_ready_2026-05-07.sqlite`다.

이 DB는 분석 전 준비용 source of truth로 사용한다. JSON은 전달용 export이며, 범위/정책 판단은 SQLite 테이블을 우선한다.

필터 정책은 `signal_filter_policy` 테이블에 남긴다. waveform 처리 코드를 만들 때 이 테이블과 `docs/filtering_policy.md`를 먼저 확인한다.

## Directory Contract

```text
data/side_loadcell_filtered_tests.csv       # 555-row filtered scope source
D:\vscode\nhtsa_metadata\data\refactor_validation_filter_ready_2026-05-07.sqlite
                                          # external full metadata DB with load-cell classification
data/side_pole_analysis_ready_2026-05-07.sqlite
                                          # 554-test analysis-ready source of truth
artifacts/harness/                        # validation JSON, QA logs, generated cohort surfaces
outputs/                                  # future analysis outputs outside the source data bundle
reports/                                  # Markdown/DOCX/dashboard exports
.agents/                                  # role-based agent instructions
.skills/                                  # repeatable procedures
.harness/                                 # validation and quality gates
```

## Gate Order

1. G0 Metadata Baseline: CSV/SQLite 구조, 건수, 코호트 재현 확인
2. G1 Raw Asset Inventory: raw waveform, 사진, 리포트 수집 상태 확인
3. G2 Channel Dictionary: 채널명, 단위, 축, 센서 위치, 샘플링 정의
4. G3 Signal QA: baseline correction, 단위 변환, filtering, time-zero 정렬
5. G4 Metrics: peak, time-to-peak, impulse, delta-V, displacement, load share 산출
6. G5 Energy Mapping: cell/zone/member energy와 근거 수준 산출
7. G6 Benchmark & Reporting: 제조사/모델 비교와 보고서/대시보드 반영

## Filtering Policy

원본 waveform은 항상 무필터 상태로 보존한다. 필터링된 force, acceleration, velocity, displacement는 별도 derived signal로 생성한다.

| 물리량 | 기본 필터 |
|---|---|
| side pole load-cell 개별 force | CFC 60 |
| side pole load-cell total force | CFC 60 |
| VEHICLE CG acceleration | CFC 60 |
| velocity/displacement 적분용 acceleration | CFC 180 |
| velocity/displacement 결과 | CFC 180 |
| 원본 waveform | 무필터 상태로 보존 |

## Editing Rules

- 원본 DB와 원본 CSV/JSON은 직접 수정하지 않는다.
- 분석 준비 DB는 `scripts/build_side_pole_analysis_ready.py`로 재생성한다.
- 새 분석 산출물은 `outputs/` 또는 명시된 `data/*analysis*` 경로에 둔다.
- 검증 없이 행 수, subset 수치, 제외 사유를 바꾸지 않는다.
