# .agents

이 디렉터리는 NHTSA 측면 충돌 분석 프로젝트를 역할 기반으로 운영하기 위한 에이전트 지침 모음입니다.

## 사용 방법

- `registry.yaml`에서 전체 에이전트 순서와 입출력 계약을 확인합니다.
- 각 `.md` 파일은 해당 역할의 작업 지시서입니다.
- 복수 에이전트가 같은 산출물을 수정하지 않도록 handoff 단위를 지킵니다.
- 최종 산출물 반영 전에는 `.harness` 검증을 실행합니다.

## 역할 요약

| 에이전트 | 핵심 역할 |
|---|---|
| 00_project_director | 범위·우선순위·게이트 관리 |
| 01_data_contract_auditor | CSV/SQLite 데이터 계약과 코호트 재현 |
| 02_raw_time_history_ingestion | NHTSA raw 파일 수집·asset inventory |
| 03_channel_dictionary_normalizer | 채널명·단위·축·센서 위치 정규화 |
| 04_signal_processing_qa | force/acceleration 신호처리와 QA |
| 05_loadcell_energy_mapper | 하중 분포·에너지·부재 매핑 |
| 06_vehicle_benchmark_analyst | 제조사·모델·차종별 비교 분석 |
| 07_report_dashboard_builder | 보고서·대시보드·표준 산출물 |
| 08_harness_regression_engineer | 테스트·회귀·품질 게이트 자동화 |
