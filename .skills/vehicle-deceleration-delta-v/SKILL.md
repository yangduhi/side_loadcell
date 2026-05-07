# Skill — Vehicle Deceleration, Delta-V & Relative Displacement

## When to use

차체 감가속도 채널이 사용 가능 상태로 정규화된 뒤 사용한다.

## Inputs

- `data/processed/channel_dictionary.csv`
- acceleration-time signal files
- impact speed and vehicle metadata

## Procedure

1. acceleration channel 로드
2. acceleration 단위 m/s²로 통일
3. sensor location과 axis 확인
4. baseline correction
5. time-zero 정렬
6. ΔV 적분 및 drift correction
7. 상대변위 산출 또는 displacement 채널과 reconcile
8. force-time과 시간축 동기화
9. QA status와 drift correction method 기록

## Outputs

- `data/derived/vehicle_deceleration_metrics.csv`
- `data/derived/vehicle_motion_timeseries.csv`

## Stop conditions

단위, 축, time-zero, drift correction method가 불명확하면 ΔV/변위 결과를 blocked 처리한다.
