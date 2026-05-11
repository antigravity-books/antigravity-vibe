---
name: mail_summary_dashboard
description: 지정된 날짜의 Outlook 수신 메일을 가져와 주제별로 요약된 대시보드를 생성하고, 세부 메일 본문을 제공하는 스킬입니다.
---

# mail_summary_dashboard

이 스킬은 로컬 Outlook 애플리케이션에 접근하여 특정 날짜에 수신된 메일들을 수집한 후, 주제 및 종류별로 분류하여 요약 대시보드를 보여줍니다. 또한 사용자가 특정 종류나 특정 메일의 원본을 요청할 경우 해당 본문을 출력합니다.

## 디렉토리 구조
- `scripts/`: 이메일 수집을 위한 파이썬 스크립트(`fetch_outlook_mails.py`) 보유
- `examples/`: 대시보드 출력 예시(`dashboard_example.md`) 

## 사전 준비 (가상 환경 설정)
이 스킬은 내부적으로 `uv`를 사용한 가상환경 및 `pywin32` 패키지가 필요합니다. 최초 실행 전 또는 환경 구성이 안 되어 있을 경우 아래 명령어를 통해 환경을 구성하세요. (반드시 `cmd /c` 사용)

```bash
cmd /c "cd C:\Users\USER\.gemini\antigravity\skills\mail_summary_dashboard\scripts && uv venv .venv && uv pip install pywin32"
```

## 스킬 실행 절차

### Step 1: 메일 수집 날짜 확인 (사용자 입력)
사용자에게 어떤 날짜의 메일을 요약할 것인지 먼저 묻습니다. 사용자가 이미 날짜를 지정했다면 이 단계를 건너뜁니다.
- 예: `2026-04-09` 형식의 날짜

### Step 2: 스크립트 실행 및 데이터 추출
다음 명령어를 실행하여 해당 날짜의 메일을 수집하고 JSON 파일로 저장합니다. 
`cmd /c` 명렁어를 활용하여 스킬의 가상환경 안에서 스크립트가 구동되도록 합니다. 

```bash
cmd /c "cd C:\Users\USER\.gemini\antigravity\skills\mail_summary_dashboard\scripts && .venv\Scripts\python fetch_outlook_mails.py --date "YYYY-MM-DD" --out "emails.json""
```
(경로: `C:\Users\USER\.gemini\antigravity\skills\mail_summary_dashboard\scripts\emails.json` 에 결과가 저장됩니다.)

실행 후 `emails.json` 파일을 분석하여 수신된 메일들의 상세 데이터를 파악합니다.

### Step 3: 요약 대시보드 생성
읽어들인 `emails.json`의 내용을 바탕으로 AI가 메일들의 본문 내용을 파악하여, 메일의 주제와 종류를 판단합니다 (예: 업무보고, 구매요청, 공지사항, 기타 등). 이를 바탕으로 **분류별 요약 대시보드**를 생성하여 사용자에게 제공합니다.
- 대시보드 출력 형태는 `examples/dashboard_example.md`의 구조를 참고하세요.
- 각 메일의 ID와 요약 내용이 반드시 포함되어야 합니다. 
- 출력의 제일 마지막에는 사용자가 특정 종류나 ID를 지정하여 **원본**을 확인할 수 있도록 안내 문구를 추가합니다.

### Step 4: 메일 본문 원본 제공 (사용자 추가 요청 시)
대시보드를 확인한 사용자가 "구매 관련 메일 원본 줘" 또는 "2번 메일 원본 확인해줘"라고 추가로 요청하면, 이전 Step에서 확인한 `emails.json`의 `body` 필드를 참고하여 요청 조건에 맞는 메일의 **본문 원본 전체**를 포맷팅하여 제공합니다.
