# Agent 03 — Channel Dictionary Normalizer

## 미션

raw time-history 파일의 채널명, 센서 위치, 축, 단위, 샘플링 정보를 표준화한다. 로드셀 배리어 force channel과 차체 감가속도 channel을 분리하고, 계산 가능한 채널만 downstream으로 넘긴다.

## 입력

- `data/processed/raw_asset_inventory.csv`
- raw time-history file headers
- SQLite `instrumentation_channels` 또는 추후 적재 결과

## 표준 분류

| measurement_type | 예시 | 필수 단위 |
|---|---|---|
| barrier_force | side pole load cell force | N 또는 kN에서 N으로 통일 |
| vehicle_acceleration | 차체/CG/rocker/pillar acceleration | g 또는 m/s²에서 m/s²로 통일 |
| displacement | 변위 또는 crush 관련 채널 | m 또는 mm에서 m으로 통일 |
| velocity | 속도 | m/s로 통일 |
| unknown | 해석 불가 | downstream 계산 제외 |

## 정규화 규칙

- `test_no`, `file_id 또는 local_path`, `raw_channel_code`, `normalized_channel_code`를 모두 보존한다.
- 단위가 불명확하면 `qa_status=blocked_unit_unknown`으로 설정한다.
- 축이 불명확하면 `axis=unknown`으로 두고 ΔV 계산 대상에서 제외한다.
- load cell 번호 또는 위치가 불명확하면 energy mapping confidence를 `low`로 설정한다.

## 산출물

- `data/processed/channel_dictionary.csv`
- `artifacts/harness/channel_dictionary_qa.json`

## 완료 조건

- force channel과 acceleration channel이 구분되어야 한다.
- 단위 변환 가능 여부가 명시되어야 한다.
- G3로 넘길 채널은 `qa_status=usable`이어야 한다.
