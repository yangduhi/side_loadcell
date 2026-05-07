# Project Instructions

항상 한국어로 답변한다. 영어 요청이 있으면 그 언어로 전환한다.

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
