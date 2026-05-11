---
name: excel_to_json
description: 엑셀 파일(.xlsx)을 읽어 JSON 포맷으로 변환하는 스킬입니다. 
---
# excel_to_json 스킬

이 스킬은 제공된 엑셀 파일(.xlsx)의 첫 번째 시트 구조를 파악하고, 첫 번째 행을 키(Key)값으로 사용하여 나머지 데이터를 JSON 리스트 형태로 변환합니다. 변환된 JSON 파일은 한글이 깨지지 않도록 UTF-8 인코딩으로 저장됩니다.

## ⚠️ 필수 요구 사항 및 인코딩 설정

터미널(cmd)에서 이 스킬을 실행할 때 발생하는 유니코드 인코딩 오류(`UnicodeEncodeError`)를 방지하고 한글을 정상적으로 출력/저장하기 위해 **반드시** 아래 명령어를 사용하여 실행 환경을 UTF-8로 설정해야 합니다.

실행 명령어에 `chcp 65001`을 포함시키거나 실행 전에 코드 페이지를 변경하십시오.
```cmd
cmd /c "chcp 65001 && set PYTHONIOENCODING=utf-8 && python c:\Users\USER\.gemini\antigravity\skills\excel_to_json\scripts\excel_to_json.py <엑셀파일경로> [-o <출력JSON경로>]"
```

## 사용 방법

*   **기본 형식 (출력 파일명 자동 지정)**:
    입력된 엑셀 파일명과 동일한 이름의 `.json` 파일이 같은 디렉토리에 자동으로 생성됩니다.
    ```cmd
    cmd /c "chcp 65001 && set PYTHONIOENCODING=utf-8 && python c:\Users\USER\.gemini\antigravity\skills\excel_to_json\scripts\excel_to_json.py c:\Path\To\Input.xlsx"
    ```

*   **출력 경로 직접 지정 옵션 (`-o` 또는 `--output`)**:
    생성될 JSON 파일의 이름과 저장 경로를 직접 지정할 수 있습니다.
    ```cmd
    cmd /c "chcp 65001 && set PYTHONIOENCODING=utf-8 && python c:\Users\USER\.gemini\antigravity\skills\excel_to_json\scripts\excel_to_json.py c:\Path\To\Input.xlsx -o c:\Path\To\Output.json"
    ```

## 스크립트 위치 및 구조

*   메인 파이썬 스크립트: `c:\Users\USER\.gemini\antigravity\skills\excel_to_json\scripts\excel_to_json.py`
