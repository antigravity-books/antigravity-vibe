---
name: analyze_monitor_prices
description: 다나와 43인치 모니터 크롤링 결과를 바탕으로 경쟁사 가격 및 사양 비교 분석을 수행하고 시각화 자료와 보고서 초안을 생성합니다. (uv 환경 사용)
---
# analyze_monitor_prices

## 역할
경쟁사(삼성전자, LG전자 등)의 가격 비교 분석 리포팅, 사양별 비교(주사율, 패널, 해상도 등), 사양별 가격 분석, 시각화 자료 생성을 목적으로 합니다. 생성된 자료는 팀장님 보고용 메일에 첨부됩니다.

## 실행 방법
1. 프로젝트의 uv 가상환경 상태에서 `Scripts/analyze_danawa.py` 스크립트를 실행합니다.
   - 원활한 실행을 위해 사전에 패키지(pandas, matplotlib, seaborn)가 설치되어 있어야 합니다. (필요 시 `uv pip install pandas matplotlib seaborn` 실행)
   - 인자로 분석할 CSV 파일의 경로와 결과물을 저장할 경로를 전달할 수 있습니다.
   - 예: `uv run python .agents\skills\analyze_monitor_prices\Scripts\analyze_danawa.py --input "Scraping_Result\danawa_43inch_monitors_20260329.csv" --output_dir "Scraping_Result"`
2. 스크립트 실행 후 옵션으로 지정한 경로에 시각화 결과물(PNG 파일)과 분석 요약 결과(`analysis_summary.csv`)가 생성됩니다.
3. `examples/report_email_template.md` 파일을 활용하여 팀장님께 보고할 메일 내용을 작성 및 전송합니다.

## 포함된 파일
- `Scripts/analyze_danawa.py`: CSV 데이터를 정제하고, 사양(해상도, 주사율, 패널)을 파싱하여 제조사별/사양별 가격을 분석 및 시각화하는 파이썬 코드.
- `examples/report_email_template.md`: 팀장님께 분석 결과를 보고하기 위한 이메일 양식 초안.
