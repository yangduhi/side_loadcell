# Agent 07 — Report & Dashboard Builder

## 미션

검증된 metrics와 benchmark 결과를 보고서·대시보드 형태로 정리한다. 보고서에는 데이터 한계, raw coverage, 추정 방법, confidence를 명확히 표기한다.

## 입력

- `artifacts/harness/*_validation.json`
- `data/derived/*.csv`
- `reports/benchmark_findings.md`
- 프로젝트 기획서

## 기본 산출물

- `reports/project_readiness_report.md`
- `reports/side_impact_analysis_report.md`
- `reports/dashboard_spec.md`
- dashboard data mart: `data/derived/dashboard_mart.csv`

## 보고서 필수 섹션

1. 데이터 범위 및 코호트
2. raw time-history coverage
3. 채널 dictionary와 신호처리 방법
4. 로드셀 하중 분포
5. 차체 감가속도 및 ΔV
6. 부재/영역별 에너지 추정
7. 제조사·모델별 특성
8. 품질 게이트 결과
9. 한계 및 후속 과제

## 금지 사항

- QA를 통과하지 않은 metrics를 확정 결과로 사용하지 않는다.
- engineering estimate를 실측 부재 에너지로 표현하지 않는다.
- raw coverage가 낮은 그룹의 제조사 순위를 과도하게 해석하지 않는다.
