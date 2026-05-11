---
name: json_to_csv
description: JSON 형태의 데이터를 CSV 파일로 저장합니다. 대상 파일이 이미 존재할 경우, 기존 데이터를 유지한 채로 새로운 데이터를 누적하여 추가(Append)합니다.
---

# json_to_csv 스킬

이 스킬은 제공된 JSON 데이터(배열 객체 형식)를 지정한 CSV 파일에 저장하거나 누적할 때 사용합니다.
작업 시 사전에 준비된 파이썬 스크립트(`scripts/json_to_csv.py`)를 활용하여 데이터를 변환하고 저장하세요.

## 스크립트 절대 경로
`C:\Users\USER\.gemini\antigravity\skills\json_to_csv\scripts\json_to_csv.py`

## 사용 방법 (Workflow)

1. **임시 JSON 파일 생성**: 저장하고자 하는 JSON 데이터를 `write_to_file` 도구를 사용하여 임시 형태의 `.json` 파일로 먼저 디스크 상에 저장합니다.
2. **스크립트 실행**: `run_command` 도구를 사용하여 파이썬 스크립트를 실행합니다. (사용자 글로벌 규칙에 따라 무조건 `cmd /c` 를 사용해야 합니다.)

   **명령어 예시**:
   `cmd /c python C:\Users\USER\.gemini\antigravity\skills\json_to_csv\scripts\json_to_csv.py "대상_CSV_파일절대경로" "입력_JSON_파일절대경로"`

   - `대상_CSV_파일절대경로`: 변환된 데이터를 저장하거나 누적할 CSV 파일의 위치.
   - `입력_JSON_파일절대경로`: 앞서 1번 단계에서 만든 임시 `.json` 파일의 위치.

3. **정리 작업**: 변환 및 저장이 완료되면 임시로 생성했던 JSON 입력 파일을 삭제하거나 무시합니다.

## 규칙 및 특징 (기능 설명)
- **자동 파일 생성 및 헤더 구성**: 대상 CSV 파일이 존재하지 않는 경우 자동으로 신규 생성하고, JSON 키를 열(Column) 헤더로 작성합니다.
- **데이터 누적 (Append)**: 기존 대상 파일이 있다면 내용을 덮어쓰지 않고, 파일 끝에 데이터를 추가합니다.
- **한글 인코딩 지원**: `utf-8-sig` 기반으로 저장되므로 엑셀 등에서 열었을 때 한글이 깨지지 않습니다.
