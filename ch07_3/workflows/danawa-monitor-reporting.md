---
description: 다나와 43인치 모니터 정보를 크롤링하고 가격과 사양을 분석하여 팀장님께 보고하는 워크플로우
---

# 다나와 43인치 모니터 시장 조사 및 보고 (danawa-monitor-reporting)

이 워크플로우는 다나와에서 43인치 삼성/LG 모니터의 가격과 사양 정보를 수집하고, 수집된 데이터를 통해 경쟁사 시장 분석을 수행한 뒤 분석 결과(차트 및 보고서)를 팀장님께 메일로 보고하는 과정을 자동화합니다.

## 실행 단계

### 1단계: 다나와 모니터 정보 수집 (Crawl)
다나와 웹사이트에서 삼성전자와 LG전자의 상위 인기 43인치 모니터 정보를 수집하여 CSV로 저장합니다. 

// turbo
1. 터미널에서 다음 명령어를 실행하여 크롤링을 수행합니다.
   ```bash
   cmd /c uv run python ".agents\skills\crawl_danawa_monitors\Scripts\danawa_crawler.py"
   ```
   * **결과물**: `Scraping_Result\danawa_43inch_monitors_YYYYMMDD.csv` 파일 생성 (YYYYMMDD는 오늘 날짜)

### 2단계: 시장 분석 및 시각화 (Analyze)
수집된 데이터를 분석하여 경쟁사별 가격 및 사양 비교 차트와 요약 보고서를 생성합니다.

// turbo
2. 크롤링된 CSV 파일을 대상으로 분석 스크립트를 실행합니다. (파일명의 날짜 부분에 주의하십시오)
   ```bash
   cmd /c uv run python .agents\skills\analyze_monitor_prices\Scripts\analyze_danawa.py --input "Scraping_Result\danawa_43inch_monitors_20260329.csv" --output_dir "Scraping_Result"
   ```
   * **결과물**: `analysis_summary.csv` 및 다수의 시각화 차트(PNG) 파일들이 `Scraping_Result` 폴더 내에 생성됩니다.

### 3단계: 보고 메일 초안 작성 (Draft Report)
분석 결과를 바탕으로 팀장님께 보고할 메일 내용을 구성합니다. 분석 결과 중 핵심 인사이트를 요약하고 시각화 차트를 메일 본문에 포함해야 합니다.

3. `analysis_summary.csv`를 읽고 주요 데이터를 파악하여 보고서 내용을 작성하십시오.
4. 생성된 시각화 차트(PNG 파일들)를 이메일 본문에 삽입할 수 있도록 준비하십시오.

### 4단계: 메일 발송 및 사용자 최종 확인 (Review & Send)
메일 발송 스킬을 사용하여 최종 보고를 수행합니다.

5. `@/send_outlook_mail` 도구를 활용하여 메일을 발송합니다.
   * **필수**: 메일 발송 전 반드시 사용자에게 제목과 작성된 본문 내용을 보여주고 최종 승인을 받은 후 발송을 승인하십시오.
