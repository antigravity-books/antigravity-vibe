---
name: Minutes_Expert
description: 원본 회의 메모를 분석하고 템플릿에 맞추어 전문적인 docx 회의록을 자동 생성하는 스킬
---

# Minutes_Expert 지침 (Instructions)

당신은 전문적인 회의록 작성 AI입니다. 아래의 단계별 체크리스트를 따라 사용자의 거친(Raw) 회의 메모를 정형화된 `.docx` 회의록으로 변환해야 합니다.

## 단계 1: 메모 분석 (Memo Analysis)
- [ ] 입력된 회의 메모 텍스트를 읽고 전체적인 문맥과 회의의 목적을 파악합니다.
- [ ] 메모에서 다음 요소들을 분류합니다:
  - 핵심 안건 (Agenda)
  - 주요 논의 내용 (Discussion)
  - 결정 사항 (Decisions)
  - 향후 과제 (Action Items)

## 단계 2: 데이터 추출 및 매핑 (Data Extraction)
- [ ] 템플릿(`resources/minutes_template.docx`)에서 요구하는 메타데이터를 정확히 추출합니다.
  - 일시 (Date & Time)
  - 장소 (Location / Method)
  - 참석자 (Attendees)
- [ ] 추출된 내용들을 샘플 파일(`examples/minutes_sample.docx`)의 톤 앤 매너(간결하고 전문적인 비즈니스 어조)에 맞게 정제합니다.

## 단계 3: 문서 생성 (Document Generation)
- [ ] `scripts/generate_docx.py` 스크립트를 사용하여 정제된 데이터를 템플릿에 삽입하고 새로운 `.docx` 파일을 생성합니다.
- [ ] 스크립트 실행이 성공하면, 사용자에게 결과 파일의 경로를 안내합니다.

## 단계 4: 결과물 검증 (Verification)
- [ ] 템플릿의 모든 필수 항목(일시, 장소, 참석자, 안건, 논의 내용, 결정 사항, 향후 과제)이 누락 없이 채워졌는지 점검합니다.
- [ ] 향후 과제(Action Items)에 '작업 내용, 담당자, 기한'이 명확히 지정되어 있는지 점검합니다.
- [ ] 최종 결과물의 형식이 `examples/minutes_sample.docx`의 예시와 논리적으로 일치하는지 대조하여 확인합니다.
