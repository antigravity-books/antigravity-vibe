---
name: generate_pptx_skill
description: JSON 형태의 슬라이드 데이터와 주제를 바탕으로 비즈니스용 이미지를 자동 생성하고, 지정된 양식(실습양식.pptx)에 맵핑하여 완성된 PPTX 파일을 생성하는 스킬입니다.
---

# Generate PPTX Skill

이 스킬은 사용자가 제공한 슬라이드 텍스트 데이터를 바탕으로 프레젠테이션용 이미지를 자동 생성하고, `python-pptx` 기반 파이썬 스크립트를 구동하여 최종 PPT 파일을 만들어냅니다. 

## 📋 핵심 수행 지침 (Agent Instructions)

### 1. 입력 데이터 확인
- 사용자가 "자료 조사 결과" 또는 "슬라이드 텍스트 내용 목록"을 제공합니다.
- Agent는 해당 내용을 파싱하여 스킬의 `resources/placeholders.json` 구조(Key)에 맞게 텍스트 교체 매핑 데이터를 구성합니다.

### 2. 비즈니스 스타일 이미지 자동 생성 및 배치
슬라이드에 삽입될 기본 이미지 4장(개요, 전략1, 전략2, 전략3)을 Agent의 \`generate_image\` 툴을 사용해 자동 생성합니다.
- **프롬프트 기본 지침:** 
  "A conceptual, modern, minimalist business illustration for [슬라이드 내용/주제]. Professional corporate style, 3D isometric, premium aesthetic, blue and gray color palette. NO TEXT, NO LETTERS."
- **이미지 저장:** 생성된 이미지를 대상 프로젝트의 특정 폴더(예: `Image/`)에 영어 파일명(overview.png, strategy1.png 등)으로 이동 또는 복사합니다.

### 3. JSON 데이터 파일 생성 (input.json)
파이썬 스크립트에 값을 넘길 매핑용 `input.json`을 작성해 사용자 프로젝트 폴더에 임시로 저장합니다.
- 구조 예시:
  ```json
  {
      "text_replacements": {
          "{{날짜}}": ["2026.04.15"],
          "{{제목}}": ["AI 에이전트 도입 전략"],
          "{{상세목차1}}": ["목차1 내용", "목차2 내용", "목차3 내용"]
      },
      "image_replacements": {
          "{{개요에 대해 설명할 수 있는 이미지}}": "C:\\절대경로\\Image\\overview.png",
          "{{전략1에 대한 이미지}}": "C:\\절대경로\\Image\\strategy1.png"
      }
  }
  ```

### 4. 스크립트 실행
본 스킬 폴더 내장 파이썬 스크립트(\`scripts/generate_ppt.py\`)를 실행합니다.
- **실행 환경:** 스위치 폴더 내의 `uv` 가상환경
- **명령어 예시:** 
  \`cmd /c "cd /d C:\Users\USER\.gemini\antigravity\skills\generate_pptx_skill && uv run scripts\generate_ppt.py --input <input.json의절대경로> --output <완성본저장경로.pptx>"\`

### 5. 완료 안내
- 파일 저장이 완료되면 사용자에게 성공 여부와 완성된 PPT 파일의 경로를 알려줍니다.
