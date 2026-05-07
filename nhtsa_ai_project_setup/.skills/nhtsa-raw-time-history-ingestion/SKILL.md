# Skill — NHTSA Raw Time-History Ingestion

## When to use

force-time, acceleration-time, ΔV, impulse, energy 분석을 시작하기 전 사용한다.

## Inputs

- `data/processed/side_pole_vtp_cohort.csv`
- NHTSA raw time-history 파일
- 시험 리포트, 사진, 영상 asset

## Procedure

1. 시험번호별 asset 검색 또는 반입
2. raw signal/report/photo/video/unknown으로 분류
3. checksum, size, local path 기록
4. header 파싱 가능 여부 표시
5. 시험번호별 coverage 산출
6. 누락 asset backlog 작성

## Output schema

`data/processed/raw_asset_inventory.csv`

```text
test_no,asset_kind,file_role,source_url,local_path,file_ext,size_bytes,checksum_sha256,status,parser_hint,qa_notes
```

## Quality gate

G1 Raw Asset Inventory.

## Stop conditions

raw signal asset이 없으면 신호처리와 energy 산출을 진행하지 않는다.
