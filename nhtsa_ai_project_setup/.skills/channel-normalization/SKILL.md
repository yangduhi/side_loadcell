# Skill — Channel Normalization

## When to use

raw time-history 파일 header를 읽은 뒤, 계산 가능한 채널을 확정할 때 사용한다.

## Inputs

- `data/processed/raw_asset_inventory.csv`
- raw file headers
- optional SQLite `instrumentation_channels`

## Procedure

1. raw channel code와 label 추출
2. measurement_type 분류: barrier_force, vehicle_acceleration, displacement, velocity, unknown
3. sensor location, axis, unit, sample_rate, cfc_class 파싱
4. project standard unit으로 변환 가능 여부 확인
5. polarity와 sign convention 기록
6. usable/blocked status 부여

## Output schema

`data/processed/channel_dictionary.csv`

```text
test_no,local_path,raw_channel_code,raw_channel_label,normalized_channel_code,measurement_type,sensor_location_code,sensor_location_label,axis,raw_unit,normalized_unit,sample_rate_hz,time_step_sec,cfc_class,polarity,qa_status,qa_notes
```

## Quality gate

G2 Channel Dictionary.
