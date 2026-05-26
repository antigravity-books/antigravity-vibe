---
name: crawl_danawa_monitors
description: 다나와(Danawa) 웹사이트에서 43인치 모니터를 검색하고 삼성전자와 LG전자의 상위 10개 인기 상품을 크롤링하여 CSV로 저장합니다.
---

# 다나와 43인치 모니터 크롤링 (crawl_danawa_monitors)

이 스킬은 다나와에서 특정 조건(43인치 모니터, 삼성/LG, 단종 제품 제외, 광고 제품 제외)에 맞는 상위 인기 상품 정보를 스크래핑하여 `Scraping_Result` 디렉토리에 CSV 포맷으로 저장하는 기능을 제공합니다. 

`implementation_plan.md` 문서에 기반하여 작성되었으며, 동적 웹 구동 제어를 위해 Selenium을, HTML 파싱을 위해 BeautifulSoup를 사용합니다.

## 사전 준비 (Prerequisites)
이 스크립트를 사용하려면 앞서 구성하신 가상 환경(UV 환경 등)과 필수 파이썬 패키지를 먼저 설치해야 합니다.

```bash
# 가상환경 프로젝트 안에서 필수 라이브러리 설치
uv pip install selenium beautifulsoup4 pandas
```

## 스크립트 실행 방법 (Usage)
작업 중인 `ch7_3` 프로젝트 메인 경로에서 아래 터미널 명령어를 실행하여 크롤링 스크립트를 작동시킵니다.
이 스킬의 핵심 코드는 스킬 내부 `Scripts` 폴더 안에 위치해 있습니다.

```bash
uv run python ".agents\skills\crawl_danawa_monitors\Scripts\danawa_crawler.py"
```

위 명령어를 실행하면 브라우저가 자동으로 실행 및 제어되며, 완료 시 메인 프로젝트 경로의 `Scraping_Result` 폴더 안에 오늘 날짜가 적용된 파일(`.csv`)이 결과물로 생성됩니다.

## 동작 원리 (How it works)
1. **브라우저 드라이버 시작**: 오류 방지를 위해 백그라운드 Headless 모드로 크롬 브라우저를 실행합니다.
2. **다나와 검색 접속**: 통합검색 쿼리스트링 `query=43인치+모니터`으로 검색 결과에 진입합니다.
3. **삼성전자 필터링**: 라벨(`label.srch_lb`) 요소 중 '삼성전자'를 찾아 클릭한 후, ajax 갱신을 위해 4초간 대기합니다.
4. **목록 스크래핑**: 목록 요소 `.prod_item`을 순회하면서 광고(`ad_item`, `ad`, `product-pot`)와 단종/품절된 제품을 건너뛴 뒤, 순수 상품들을 10개까지 추출합니다. 추출 항목은 (크롤링 시간, 제조사, 상품명, 사양, 모델 가격)입니다.
5. **LG전자 필터링 및 스크래핑**: 새 통합검색 화면으로 리로드하여 필터를 초기화한 후 'LG전자' 라벨을 클릭하여 동일한 방식으로 상위 10개를 갱신하고 스크래핑합니다.
6. **CSV 저장 (`Scraping_Result/`)**: 추출된 전체 20개의 항목을 Pandas DataFrame으로 변환 후, 엑셀에서 바로 열 수 있도록 UTF-8(BOM 포함)을 적용한 CSV 파일로 저장합니다.
