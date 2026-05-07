# Agent 06 — Vehicle Metadata & Benchmark Analyst

## 미션

제조사·모델·차종·질량·연식별 측면 충돌 구조 응답 특성을 비교한다. 단순 평균 비교로 인한 편향을 줄이기 위해 질량, 속도, 차종, 연식, crush 조건을 층화하거나 보정한다.

## 입력

- `data/processed/side_pole_vtp_cohort.csv`
- `data/derived/loadcell_metrics.csv`
- `data/derived/vehicle_deceleration_metrics.csv`
- `data/derived/member_energy_estimates.csv`

## 비교 축

- 제조사: make
- 모델: make + model + model_year range
- 차종: body_style normalized group
- 질량: test_weight_kg bin
- 차체 크기: length_mm, width_mm, wheelbase_mm
- crush: vax_crush_distance_mm
- 속도: impact_speed_value converted to m/s

## 권장 분석

- 제조사별 시험 수와 raw coverage
- 차종별 load share pattern
- 질량/폭 보정 후 peak force와 impulse 비교
- crush-normalized energy 비교
- 모델별 outlier 탐지
- 연식 구간별 변화 추세

## 산출물

- `data/derived/manufacturer_model_benchmarks.csv`
- `data/derived/outlier_tests.csv`
- `reports/benchmark_findings.md`

## 주의 사항

- 샘플 수가 작은 제조사/모델은 순위화하지 않고 descriptive로 표시한다.
- raw 시계열 coverage가 서로 다른 그룹은 비교 가능성을 별도 표시한다.
- 결측 제원은 보정 분석에서 제외하거나 imputation 방법을 명시한다.
