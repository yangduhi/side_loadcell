# Agent 04 — Signal Processing & QA

## 미션

로드셀 force-time과 차체 acceleration-time 신호를 전처리하고, peak, impulse, ΔV, 상대변위 등 기본 metrics를 산출한다.

## 입력

- `data/processed/channel_dictionary.csv`
- raw time-history files
- `.harness/config.yaml`의 signal_processing 설정

## 처리 절차

1. raw signal 로드 및 time vector 생성
2. 단위 변환: force → N, acceleration → m/s², time → s
3. pre-impact baseline correction
4. time-zero 정렬: force threshold 또는 명시된 trigger 기준
5. filtering 설정 적용 및 filter metadata 기록
6. saturation, missing, non-monotonic time, sample-rate mismatch 점검
7. force channel별 peak, time-to-peak, impulse 산출
8. acceleration channel별 peak, ΔV, drift-corrected displacement 산출

## 기본 산출 metrics

- `peak_force_n`
- `time_to_peak_ms`
- `impulse_n_s`
- `force_duration_ms`
- `peak_accel_mps2`
- `delta_v_mps`
- `relative_displacement_m`
- `qa_status`

## 산출물

- `data/derived/loadcell_metrics.csv`
- `data/derived/vehicle_deceleration_metrics.csv`
- `artifacts/harness/signal_qa_summary.json`

## 금지 사항

- 단위 미확인 채널을 계산에 사용하지 않는다.
- time-zero 미정렬 신호를 시험 간 비교에 사용하지 않는다.
- drift correction 방법을 기록하지 않은 ΔV/변위 결과를 보고서에 반영하지 않는다.
