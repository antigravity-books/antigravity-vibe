# 10.1 Prompt 1:
역할 부여: 당신은 숙련된 풀스택 웹 개발자입니다. 빠르고 효율적인 Python 웹 프레임워크인 FastAPI를 사용하여 '사내 회의실 예약 시스템'을 만들어주세요.
기술 스택:
언어: Python 3.12+
패키지 관리: uv (적극 권장)
웹 프레임워크: FastAPI
데이터베이스: SQLModel (SQLite 개발용, PostgreSQL 배포용)
템플릿 엔진: Jinja2
스타일링: TailwindCSS (CDN 사용)
구현 요구사항:
1.데이터베이스 모델 (Reservation)
- id: 고유 번호
- reserver_name: 예약자 이름
- room_name: 회의실 이름 (예: '대회의실', '미팅룸A' 등)
- start_time: 시작 시간 (9시~18시 사이의 정수)
- end_time: 종료 시간 (시작 시간 + 1시간으로 고정)
2. 기능 및 라우트
GET /: 메인 현황판. 9시부터 18시까지, 각 회의실별 예약 현황을 한눈에 볼 수 있는 시간표(Grid) 형태로 보여주세요. 예약된 칸은 색깔로 표시하고 예약자 이름을 보여줍니다.
POST /reserve: 예약 하기. 이름, 회의실, 시간을 선택하여 예약을 저장합니다. 단, 이미 예약된 시간에 중복 예약하는 것을 막아주세요.
3. UI 디자인
TailwindCSS를 사용하여 깔끔하고 직관적인 '대시보드' 스타일로 만들어주세요.
좌측에는 예약 입력 폼, 우측에는 실시간 예약 현황표를 배치해주세요.
4. 배포 준비
Railway 등 클라우드 배포를 위해 Procfile과 runtime.txt를 포함해주세요.
데이터베이스 연결(DATABASE_URL)은 환경 변수를 우선 사용하고, 없으면 로컬 SQLite를 사용하도록 
database.py를 구성해주세요.


# 10.4 Prompt 1:
기능 구현이 끝났어. 이제 Railway 배포를 위한 최종 설정을 마무리해줘.
처음에 배포는 고려하지 않아서 gunicorn, whitenoise은 설치되지 않았어. 이점을 고려해서 진행해줘.

[배포 설정 요구사항]
1. 의존성 설치: 
`uv add gunicorn whitenoise ` 명령어로 필요한 패키지를 먼저 설치해줘.

2. settings.py 수정:
   - `DEBUG = os.getenv('DEBUG', 'False') == 'True'` 로 변경
   - `ALLOWED_HOSTS = ['*']` (또는 `.railway.app` 도메인 허용)
   - `CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']` 추가
   - 정적 파일 설정:
     ```
     STATIC_ROOT = BASE_DIR / 'staticfiles'
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
     MIDDLEWARE에 'whitenoise.middleware.WhiteNoiseMiddleware' 추가
     ```

3. requirements.txt 생성: 
`uv export --format requirements-txt --output-file requirements.txt` 명령어로 생성

4. 검증:
`python manage.py collectstatic` 명령어로 정적 파일 설정 확인
