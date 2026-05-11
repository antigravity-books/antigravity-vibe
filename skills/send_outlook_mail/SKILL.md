---
name: send_outlook_mail
description: "JSON 포맷의 입력을 받아 Outlook 메일을 발송합니다. 내부 uv 가상환경을 사용하여 실행됩니다."
---

# send_outlook_mail

Outlook 메일을 발송하는 스킬입니다. 수신인(to), 참조자(cc), 제목(subject), 본문(body), 첨부파일(attachments)을 JSON 포맷으로 입력받아 처리합니다.

## Prerequisites
- Windows 운영체제
- Microsoft Outlook 설치 및 로그인 상태
- 내부에 구성된 고유의 uv 가상환경 (.venv)

## Virtual Environment Setup
이 스킬은 내부의 `.venv` 가상환경을 구동하여 사용합니다. 설정은 다음 명령어로 이루어집니다:
```bat
cd C:\Users\USER\.gemini\antigravity\skills\send_outlook_mail
uv venv .venv
uv pip install pywin32 --python .venv
```

## Usage
실행 시 대상 스크립트에 JSON 포맷의 이메일 데이터를 인자로 전달합니다.

### JSON 포맷 예시:
```json
{
  "to": "recipient@example.com",
  "cc": "cc@example.com",
  "subject": "메일 제목",
  "body": "메일 본문",
  "attachments": [
    "C:\\path\\abs\\to\\file.xlsx"
  ]
}
```

### 터미널 실행 방법:
한글 인코딩 문제를 방지하기 위해 터미널 실행 시 `chcp 65001`을 사용하십시오.

```bat
cmd /c chcp 65001 && "C:\Users\USER\.gemini\antigravity\skills\send_outlook_mail\.venv\Scripts\python.exe" "C:\Users\USER\.gemini\antigravity\skills\send_outlook_mail\scripts\send_mail.py" "{\"to\":\"test@test.com\", \"subject\":\"테스트\", \"body\":\"본문\"}"
```
