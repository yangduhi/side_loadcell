# Skill — Manufacturer & Model Benchmarking

## When to use

metrics와 energy estimates가 QA를 통과한 뒤 제조사·모델 특성을 비교할 때 사용한다.

## Inputs

- `data/processed/side_pole_vtp_cohort.csv`
- `data/derived/loadcell_metrics.csv`
- `data/derived/vehicle_deceleration_metrics.csv`
- `data/derived/member_energy_estimates.csv`

## Procedure

1. make/model/body_style/model_year/test_weight 기준 그룹 정의
2. raw coverage와 usable metrics coverage 확인
3. 질량·속도·폭·wheelbase·crush 분포 확인
4. small-n 그룹은 순위화 제외
5. peak force, impulse, ΔV, energy ratio, crush-normalized energy 비교
6. outlier test 목록과 원인 후보 기록
7. 제조사·모델별 특성은 보정/층화 여부를 명시

## Outputs

- `data/derived/manufacturer_model_benchmarks.csv`
- `data/derived/outlier_tests.csv`
- `reports/benchmark_findings.md`
