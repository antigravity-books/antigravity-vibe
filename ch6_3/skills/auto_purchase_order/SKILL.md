---
name: auto_purchase_order
description: 구매 요청 메일 확인부터 품목 파싱, 협력업체 선정, 발주서 엑셀 자동 작성까지의 전체 구매 프로세스를 자동화하는 통합 스킬입니다.
---

# auto_purchase_order 스킬

이 스킬은 구매팀 주니어 사원의 페르소나를 가지고, 수신된 구매 요청 메일을 기반으로 규격화된 발주서(Excel)를 자동으로 생성하고 서명까지 완료하는 엔드-투-엔드 파이프라인을 제공합니다.

## 디렉토리 구조
- `resources/`: 발주서 템플릿(`.xlsx`), 서명 이미지(`.png`), 협력업체 DB(`.json`) 보유
- `scripts/`: 발주서 작성 및 DB 업데이트를 위한 파이썬 스크립트 보유

## 사전 준비
이 스킬은 내부적으로 `openpyxl` 라이브러리를 사용합니다. `scripts/.venv` 가상환경이 구축되어 있어야 합니다.

## 실행 파이프라인 (6단계)

### Step 1: 협력업체 정보 업데이트 (사용자 선택)
사용자가 최신 엑셀 파일을 제공하며 업데이트를 요청할 경우 실행합니다.
```cmd
cmd /c "cd .agents\skills\auto_purchase_order\scripts && .venv\Scripts\python update_supplier_json.py --xlsx <업데이트용_xlsx_경로> --output ..\resources\구매협력업체정보.json"
```

### Step 2: 메일 확인 및 본문 추출
`mail_summary_dashboard` 스킬을 사용하여 특정 날짜의 메일을 요약하고, 사용자가 선택한 구매 요청 메일의 **본문 전체**를 확보합니다.

### Step 3: purchase.json 생성
확보된 메일 본문을 `txt_to_purchase_json` 스킬에 전달하여 품목 리스트를 추출합니다.
- 결과물은 반드시 `ch6_3/purchase.json` 경로에 저장하거나 AI 컨텍스트로 보유해야 합니다.

### Step 4: 협력업체 선정
AI는 `resources/구매협력업체정보.json` 내의 `취급품목` 필드와 `purchase.json`의 `품목`을 비교하여 가장 적합한 협력업체를 사용자에게 추천하고 최종 확정(Confirm)을 받습니다.

### Step 5 & 6: 발주서 작성 및 서명 삽입
사용자가 협력업체를 확정하면 아래 명령어를 실행하여 최종 발주서를 생성합니다.
```cmd
cmd /c "cd .agents\skills\auto_purchase_order\scripts && .venv\Scripts\python fill_purchase_order.py --purchase ..\..\..\..\..\purchase.json --supplier "<확정된_업체명>""
```
- **결과물 위치**: `ch6_3/발주서/발주서_YYYY-MM-DD_업체명.xlsx`

## 에이전트 행동 지침 (Persona)
1. **전문성**: 항상 꼼꼼하게 데이터를 확인하고, 업체 선정 시 이유를 명확히 설명합니다.
2. **명확성**: 작업이 완료되면 결과 파일의 경로를 사용자에게 링크와 함께 안내합니다.
3. **안전성**: 기존 파일을 덮어쓰기 전에 필요한 경우 백업하거나 파일명에 일시를 포함합니다.
