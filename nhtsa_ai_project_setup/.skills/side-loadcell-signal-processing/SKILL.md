# Skill — Side Loadcell Signal Processing

## When to use

로드셀 배리어 force-time 채널이 사용 가능 상태로 정규화된 뒤 사용한다.

## Inputs

- `data/processed/channel_dictionary.csv`
- raw force-time signal files
- `.harness/config.yaml`

## Procedure

1. force channel 로드
2. time vector 생성 및 monotonicity 확인
3. force 단위 N으로 통일
4. pre-impact baseline correction
5. time-zero 정렬
6. filtering metadata 적용 및 기록
7. cell별 peak force, time-to-peak, impulse, duration 산출
8. 총 하중, force share, load centroid 산출
9. QA status와 제외 사유 기록

## Outputs

- `data/derived/loadcell_metrics.csv`
- `data/derived/load_distribution_timeseries.csv`
- `artifacts/harness/signal_qa_summary.json`

## Quality gates

G3 Signal QA, G4 Metrics.
