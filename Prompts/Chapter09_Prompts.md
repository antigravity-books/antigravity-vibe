# 9.4 Prompt 1: 
현재 프로젝트에 uv 환경을 셋팅하고 앞으로 반드시 uv로 패키지 설치 및 코드 실행을 해줘.

# 9.4 Prompt 2: 
"Django로 'dashboard'라는 이름의 프로젝트를 시작하고 싶어.
그리고 환율 정보를 다룰 'exchange'라는 앱(App)을 만들어줘.

다음 요구사항에 맞춰서 초기 설정 가이드를 줘:
1. 프로젝트 구조는 표준 Django 형식을 따라줘.
2. settings.py에서 보안과 관련된 키(SECRET_KEY, DEBUG 등)는 .env 파일에서 불러오도록 python-dotenv를 설정해줘.

# 9.4 Prompt 3:
"이제 'exchange' 앱에서 한국수출입은행 API를 통해 실시간 환율을 가져오는 기능을 구현해줘. 간단히 한화를 입력하면 선택한 국가의 돈으로 환산해주는 기능도 넣어줘.
[API 정보]
URL: https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON
파라미터: authkey(API키), searchdate(YYYYMMDD), data('AP01')

[구현 요구사항]
보안 필수: API Key는 절대 코드에 적지 말고, .env 파일에서 API_KEY로 불러와야 해.
views.py: requests 라이브러리를 사용해서 데이터를 가져오는 index 함수를 만들어줘.
verify=False 옵션을 추가해서 SSL 에러를 방지해줘.

오늘 날짜로 요청했는데 데이터가 없으면(주말/공휴일), 최근 영업일 데이터를 가져오거나 '데이터 없음' 처리를 해줘.

urls.py: /exchange/ 경로로 접속하면 이 뷰가 보이게 연결해줘.

templates: exchange/index.html을 만들고, 받아온 환율 데이터를 깔끔한 HTML 표(Table)로 보여줘. (Tailwind CSS CDN을 사용해서 스타일링하고 별도로 css 파일로 분리 해줘)"

# 9.4 Prompt 4:
앱을 실행했더니 아래와 같이 에러가 발생해. 왜 그런거야? 

(에러 코드 복사 붙여넣기)


# 9.5 Prompt 1:
현재 프로젝트에 파이썬 버전 3.12로 된 uv 환경을 셋팅해줘. 
앞으로 하게 될 프로젝트는 Django와 Gemini API를 사용할거야. 
그리고 무조건 파이썬을 실행할 때는 uv run 명령을 사용해서 가상환경을 활용해줘


# 9.5 Prompt 2:
지금부터 'AI 뉴스 큐레이션 앱'을 만들 거야. 내가 원하는 기능은 다음과 같아. 
1. 사용자가 '검색 키워드'와 '필터링 프롬프트'를 입력한다. 
2. 네이버 검색 API로 20개의 기사를 검색한다. 
3. 검색된 기사의 제목을 보고 AI가 '필터링 프롬프트'를 참고하여 3개만 선정한다. 
4. 선정된 기사를 요약하고 화면에 출력한다. 
5. API Key는 .env 파일에 사용자가 직접 입력하고 코드에서 참조하는 방식으로 한다.

# 9.5 Prompt 3:
아래와 같은 에러가 발생했어. 고쳐줘. 
(에러 코드 복사 붙여넣기)
