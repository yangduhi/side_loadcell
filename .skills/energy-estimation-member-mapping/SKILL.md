# Skill — Energy Estimation & Member Mapping

## When to use

loadcell force metrics와 차량 motion/displacement metrics가 준비된 뒤 사용한다.

## Inputs

- `data/derived/loadcell_metrics.csv`
- `data/derived/vehicle_deceleration_metrics.csv`
- `data/processed/lcb_cell_layout.csv`
- `data/processed/member_mapping.csv`
- photo/video/report validation assets

## Procedure

1. cell force와 displacement timebase 동기화
2. cell별 `E_i = ∫F_i ds` 산출
3. zone별 force/energy aggregation
4. member mapping weight matrix 적용
5. energy ratio, specific energy, crush-normalized energy 산출
6. confidence 부여: high/medium/low/blocked
7. assumption_notes 작성

## Outputs

- `data/derived/cell_energy_estimates.csv`
- `data/derived/member_energy_estimates.csv`
- `artifacts/harness/energy_mapping_qa.json`

## Mandatory label

모든 부재별 energy 결과는 `estimate_method=engineering_estimate` 또는 동등한 명시 태그를 가져야 한다.
