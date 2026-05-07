# Agent 05 — Loadcell Energy & Member Mapper

## 미션

로드셀 하중 분포와 차체 상대변위를 결합하여 cell/zone/member 단위 에너지 흡수량을 추정한다. 부재별 에너지는 직접 계측값이 아니므로 근거 수준과 불확실성을 함께 산출한다.

## 입력

- `data/derived/loadcell_metrics.csv`
- `data/derived/vehicle_deceleration_metrics.csv`
- `data/processed/channel_dictionary.csv`
- `data/processed/lcb_cell_layout.csv`
- `data/processed/member_mapping.csv`
- 사진/영상/PDF report 검증 자료

## 계산 개념

- cell force-time: `F_i(t)`
- 영역 force: `F_zone(t) = Σ F_i(t)`
- 하중 분담률: `share_i(t) = F_i(t) / Σ F_i(t)`
- impulse: `∫F_i(t)dt`
- 에너지 추정: `E_i = ∫F_i(s) ds`
- 부재별 에너지: cell/zone-to-member weight matrix를 적용한 engineering estimate

## 근거 수준

| confidence | 조건 |
|---|---|
| high | 명시적 cell geometry + 사진/영상/리포트 검증 + 채널 단위/축 검증 완료 |
| medium | cell geometry와 채널 검증 완료, 부재 검증은 간접 근거 |
| low | cell 위치 또는 부재 매핑 불완전 |
| blocked | force 또는 displacement 산출 불가 |

## 산출물

- `data/derived/load_distribution_timeseries.csv`
- `data/derived/cell_energy_estimates.csv`
- `data/derived/member_energy_estimates.csv`
- `artifacts/harness/energy_mapping_qa.json`

## 필수 컬럼

```text
test_no,member_id,member_label,energy_j,energy_ratio,specific_energy_j_per_kg,
crush_normalized_energy_j_per_mm,estimate_method,confidence,qa_status,assumption_notes
```
