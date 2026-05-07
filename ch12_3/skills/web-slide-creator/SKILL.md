---
name: web-slide-creator
description: 바닐라 자바스크립트 기반의 고성능 웹 프레젠테이션 슬라이드를 생성, 수정 및 확장합니다. 외부 라이브러리 없이 브라우저 표준 기술(HTML5, CSS3, ES6+)만을 사용하여 16:9 비율의 반응형 시스템을 유지하며, ApexCharts 기반의 데이터 시각화와 프리미엄 UI/UX 표준을 준수합니다.
---

# 웹 슬라이드 제작사 (Vanilla Slide System v3.0)

이 스킬은 고유의 `Presentation` 클래스를 기반으로 하는 웹 프레젠테이션 시스템을 관리합니다. 모든 결과물은 외부 이미지 없이 순수 웹 코드로만 이루어진 프리미엄 디자인 표준을 따라야 합니다.

## 🏛️ 1. 핵심 아키텍처 및 레이아웃 표준

### 1.1 구조 및 비율 (16:9)
- **컨테이너**: 모든 슬라이드는 `<section class="slide" id="slide-N">` 구조를 가집니다.
- **Aspect Ratio**: `aspect-ratio: 16 / 9;` 속성을 사용하여 비율을 고정합니다.
- **반응형 스케일링**: Root font-size를 조정하여 대형 스크린 가독성을 확보합니다.
- **칼정렬 시스템**: 상단 헤더(`slide-header`)와 본문 박스(`.content`)는 반드시 **최대 너비 1300px 및 중앙 정렬(`margin: 0 auto`)** 수직 축에 정렬되어야 합니다.

### 1.2 레이아웃 기술 및 균형 정렬 (Balanced Alignment)
- **Flexbox**: 단일 슬라이드 내부의 **수평 및 수직 중앙 정렬(`justify-content: center; align-items: center;`)**에 필수적으로 사용합니다. 모든 슬라이드 콘텐츠는 시각적으로 좌우/상하 균형이 완벽해야 합니다.
- **수직적 균형 (Vertical Balance)**: 콘텐츠가 상단이나 하단으로 너무 치우치지 않도록 주의합니다. 특히 상단 배지와 제목(`slide-header`)은 슬라이드 상단 경계선에서 충분한 여백을 두어야 하며, 본문 텍스트나 카드들이 슬라이드 중앙 영역에 안정적으로 배치되도록 구성합니다.
- **CSS Grid**: 사이드바, 2/3분할 그리드 등에서 **박스 간의 균형 잡힌 간격(`gap`) 및 정렬(`align-items: center;`)**을 확보하기 위해 사용합니다.
- **고정 헤더**: 모든 슬라이단 상단에는 해당 주제를 나타내는 배지(Badge)와 제목(`h2`)이 일관된 위치에 포함되어야 하며, 상단 여백(`margin-top: 5vh;`)을 두어 답답함을 방지합니다. 하단 여유 공간은 본문 박스(`.content`)가 시각적 중심을 잡도록 배치합니다.
- **레이아웃 균등화 (Standard v4.7)**: 그리드나 플렉스 내부에 배치되는 카드 요소(`.glass-card`, `.example-box` 등)들은 텍스트 양에 상관없이 동일한 높이를 가져야 합니다. 이를 위해 `height: 100%`와 `display: flex; flex-direction: column;`을 사용하여 수직 축을 정렬합니다.

### 1.3 동적 스케일링 및 가독성 (Scale-to-Fit)
- **대화면 대응**: 루트 폰트 사이즈 조정 외에도, `transform: scale()`을 이용한 동적 스케일링 엔진을 권장합니다.
- **표준 너비**: 1400px을 기준 너비로 잡고, 브라우저 창 크기에 맞춰 `Math.min(window.innerWidth / 1400, window.innerHeight / 787.5)` 비율로 컨테이너를 확대/축소하여 공간을 꽉 채웁니다.
- **안전 여백**: 슬라이드 외곽이 잘리지 않도록 계산된 스케일 값에 **0.9~0.95(90~95%) 정도의 안전 계수**를 곱하여 적용합니다.
- **인쇄 시 주의**: 인쇄 시에는 이 스케일링이 해제되어야 하므로 `@media print`에서 `transform: none !important;` 처리가 필수입니다.

## ⚙️ 2. 네비게이션 및 인터랙션 엔진

### 2.1 이벤트 및 동기화
- **Hash 동기화**: URL Hash(`#slide-N`)를 통해 현재 위치를 관리하며, 브라우저 뒤로 가기/앞으로 가기 시에도 동기화되어야 합니다.
- **이벤트 잠금**: 애니메이션 진행 중(`isAnimating = true`)에는 중복 입력을 무시하여 버그를 방지합니다.

### 2.2 자동 순차 노출 (Automatic Sequential Reveal)
- 슬라이드 내 각 요소에는 `[data-step]` 속성을 부여합니다.
- 슬라이드 전환 직후, 해당 슬라이드 내의 모든 `data-step` 요소는 일정한 간격(예: 0.2초)을 두고 **자동으로** 노출(`.visible` 클래스 추가)되어야 합니다.
- 이는 별도의 클릭 없이도 발표의 몰입감을 높이는 프리미엄 연출 표준입니다.

## 🎨 3. 디자인 시스템 및 시각 정체성 (Premium Standard v3.5)

### 3.1 컬러 팔레트 (The Amber-Slate System)
모든 슬라이드는 다음의 색상 체계를 엄격히 준수합니다.

| 구분 | 다크 모드 (Default) | 라이트 모드 |
| :--- | :--- | :--- |
| **Base Background** | `#0f172a` (Slate 900) | `#f8fafc` (Slate 50) |
| **Secondary BG** | `#1e293b` (Slate 800) | `#f1f5f9` (Slate 100) |
| **Main Text** | `#f8fafc` (Slate 50) | `#0f172a` (Slate 900) |
| **Dim/Body Text** | `#94a3b8` (Slate 400) | `#64748b` (Slate 500) |
| **Accent (Amber)** | `#f59e0b` (Amber 500) | `#d97706` (Amber 600) |
| **Glass BG** | `rgba(30, 41, 59, 0.7)` | `rgba(255, 255, 255, 0.8)` |
| **Glass Border** | `rgba(255, 255, 255, 0.1)` | `rgba(0, 0, 0, 0.05)` |

### 3.2 타이포그래피 및 레이아웃 상수
- **표준 폰트**: `Inter` (UI/본문), `Outfit` (헤더/강조) - Google Fonts 필수.
- **Header 1 (Hero)**: **7rem ~ 8rem**, font-weight 800, line-height 1. (대화면 가독성 최우선)
- **Header 2 (Slide)**: **4rem ~ 5rem**, font-weight 800.
- **Body Text**: **1.8rem ~ 2.2rem**, line-height 1.6.
- **최대 콘텐츠 너비**: `1300px` (중앙 정렬 가이드라인).
- **슬라이드 규격**: `1400px` x `787.5px` (16:9 황금 비율).
- **디자인 밸런스**: 
  - 슬라이드 상단에서 제목까지의 여백(`margin-top`)은 **전체 높이의 약 10~15%**를 권장합니다.
  - 콘텐츠가 슬라이드 상단이나 하단에 딱 붙지 않도록 **수직적 무게 중심을 중앙 또는 약간 위에** 둡니다.
  - 본문 카드가 들어갈 경우, 하단에도 적절한 여백을 두어 '떠 있는' 느낌이 들지 않도록 합니다.

### 3.3 시각적 연출 (Visual Effects)
- **Amber 액센트**: 강조가 필요한 텍스트나 코드에는 `.highlight-amber` 클래스를 사용하여 세렴된 하이라이트 효과를 적용합니다.
- **클린 디자인 (Image-free)**: 외부 이미지를 생성(`generate_image`)하지 마십시오. 오직 **Lucide 아이콘**과 **CSS 그라데이션**, **SVG 패턴**으로만 시각적 완성도를 확보합니다.
- **글래스모피즘**: 카드/박스 요소에는 `backdrop-filter: blur(20px)`와 반투명 배경을 조합하여 프리미엄 질감을 구현합니다.
- **애니메이션 속도**: 전체 전환 `0.6s`, 순차 노출(Step) 간격 `0.3s`.

### 3.4 애니메이션 성능
- **GPU 가속**: `transform`(특히 `translate3d`)과 `opacity` 속성만 애니메이션화하여 레이아웃 리플로우(Reflow)를 방지합니다.
- **성능 힌트**: `will-change: transform;`를 사용하여 브라우저 최적화를 유도합니다.

## 📊 4. 데이터 시각화 원칙 (ApexCharts)

통계 데이터, 수치 비교, 트렌드 분석이 포함될 경우 **반드시 ApexCharts**를 사용하여 시각화합니다.
- **Bar Chart**: 성능 비교, 효율 격차 표현 (Radius 8px 권장).
- **RadialBar**: 목표 달성률, 정확도 등 단일 수치 강조.
- **Area Chart**: 시간 흐름에 따른 생산성 변화 (Spline Curve 적용).
- **차트 규격 (Standard v4.7)**: `.chart-container`는 슬라이드 가용 너비의 최대치인 `max-width: 1100px`를 유지하며, ApexCharts 옵션에서 `width: '100%'`를 명시하여 박스에 꽉 차게 렌더링합니다.
- **팔레트 동기화**: `changePalette()` 시 `chart.updateOptions()`를 호출하여 차트 색상을 실시간 동기화합니다.

## 5. PDF 내보내기 및 인쇄 표준 (PDF Export Standard v4.7.5 - Enhanced Stability)

프리미엄 웹 슬라이드 시스템은 단일 HTML 파일로 완벽한 문서화(PDF)가 가능해야 합니다. 이를 위해 테마 가변성과 렌더링 안정성을 보장합니다.

### 5.1 CSS 인쇄 최적화 (@media print)
- **ID 선택자 우선순위 (MANDATORY)**: 인쇄 엔진에서 인라인 스타일 간섭을 피하기 위해 반드시 `#presentation` ID 선택자를 사용하여 스타일을 재정의합니다.
- **슬라이드 레이아웃 (Flex Standard)**: 인쇄 시 슬라이드 본문이 사라지거나 정렬이 깨지는 것을 방지하기 위해, `.slide`는 반드시 `display: flex !important`를 유지해야 합니다. (기존 `block` 방식은 수직 중앙 정렬을 파괴할 수 있음)
- **배경색 및 테마 강제화**: 브라우저의 인쇄 설정에 관계없이 프리미엄 디자인을 유지하기 위해, `.slide`에 `background`와 `color`를 명시적으로 부여(`!important`)하고 `-webkit-print-color-adjust: exact`를 적용합니다.
- **테마 상태 동기화**: `<html>` 태그에 `data-theme="dark"`를 기본값으로 설정하여 인쇄 엔진이 CSS 변수를 안정적으로 로드하도록 권장합니다.
- **인쇄용 트랜스폼 리셋 (CRITICAL)**: 화면용으로 적용된 `transform: scale()`이 인쇄 엔진에서 레이아웃을 파괴(잘림 현상)하는 것을 막기 위해, CSS에서 `#presentation { transform: none !important; }`를 적용함과 동시에 **반드시 JS 동적 리셋**을 병행해야 합니다.
- **JS 동적 리셋 (Standard v4.7.1)**: `beforeprint`에서 `presentation.style.transform = 'none'`을 실행하고 `afterprint`에서 `initScaling()`을 재호출하여 이중으로 레이아웃 안정성을 확보합니다.
- **래퍼 리셋**: 인쇄 시 상위 컨테이너(`.presentation-wrapper`)의 Flex 정렬을 해제(`display: block !important;`)하여 슬라이드가 페이지 상단부터 정확히 배치되도록 합니다.
- **전체 슬라이드 출력 보장 (Stacking Logic)**: 인쇄 시 웹의 `position: absolute` 구조를 해제하고, 모든 슬라이드를 수직으로 쌓아 전체가 인쇄되도록 합니다. 
  - `.presentation, .slide { display: block !important; position: relative !important; height: auto !important; opacity: 1 !important; visibility: visible !important; }` (단, 개별 슬라이드 내부는 `flex` 유지)
- **콘텐츠 고정 (Fragment Freeze)**: 모든 `[data-step]` 요소의 `opacity: 1`, `transform: none`, `transition: none`을 강제하여 슬라이드의 최종 상태가 누락 없이 출력되도록 합니다.
- **인터페이스 제거**: `#hud-overlay`, `.modal-overlay`, `.shortcuts-info` 등 웹 전용 UI 요소를 인쇄 시 반드시 숨깁니다. (`display: none !important;`)

### 5.2 엔진 제어 (Chart & Animation)
- **차트 애니메이션 동결**: `exportPDF()` 호출 시, `ApexCharts`의 애니메이션을 일시적으로 비활성화(`animations: { enabled: false }`)한 후 인쇄창을 띄워 데이터가 완전히 그려진 상태로 캡처되도록 합니다.
- **레이아웃 안정성**: 인쇄 엔진에서 불안정한 `backdrop-filter: blur` 등을 제거하고, 복잡한 그리드 레이아웃은 안정적인 `flex` 기반으로 폴백(Fallback) 처리합니다.

### 5.3 사용자 안내 가이드
PDF 저장 시 최상의 품질을 위해 다음 브라우저 인쇄 설정을 안내해야 합니다.
- **배경 그래픽 (Background Graphics)**: 반드시 체크 (ON)
- **머리글과 바닥글 (Headers and Footers)**: 반드시 체크 해제 (OFF)

## 🌓 6. 테마 및 사용자 편의성 (Interaction Standard v4.6)

### 6.1 테마 시스템
- **동적 제어**: `:root` 변수를 활용하여 다크/라이트 모드를 완벽히 제어합니다.
- **타원형 토글 (Oval Toggle)**: 가로 타원 형태의 슬라이딩 스위치를 구현하여 직관적인 테마 전환을 제공합니다.

### 6.2 표준 HUD 네비게이션 (Fixed Bottom HUD)
프리미엄 프레젠테이션의 일관성을 위해 다음 구조의 하단 고정형 HUD(`id="hud-overlay"`)를 반드시 구현합니다.

- **좌측 섹션 (Identity)**:
    - **Logo**: `ANTIGRAVITY SLIDES` (브랜드 정체성 노출).
    - **Indicator**: `01 / 10` 형식의 페이지 번호 (두 자리 패딩 필수).
- **중앙 섹션 (Progress)**:
    - **Progress Bar**: 슬라이드 진행률을 시각적으로 보여주는 얇은 수평 바 (`#progress-fill`).
- **우측 섹션 (Controls)**:
    - **Oval Switch**: 테마 전환 스위치.
    - **Button Group**: `Home`, `Prev`, `Next`, `Print`, `Help` 버튼 모음.

### 6.3 단축키 및 도움말 (Help Modal Standard)
- **도움말 모달**: 상시 노출로 인한 콘텐츠 침범을 방지하기 위해 반드시 전용 모달(`id="help-modal"`) 형식을 사용합니다.
- **호출 방식**:
    - HUD 우측 끝의 `?` 버튼 클릭.
    - 키보드 `?` 또는 `/` 키 입력.
- **닫기 방식**: 모달 내 `닫기` 버튼 클릭 또는 `Escape` 키 입력.
- **콘텐츠 구성**: 시각적으로 구분된 `kbd` 태그와 설명문이 포함된 그리드 레이아웃을 권장합니다.

## 🚀 올바른 작업 흐름
1. **분석**: 데이터가 포함되었는가? (ApexCharts 준비) 강조할 내용이 있는가? (Amber 하이라이트 준비)
2. **수정**: `index.html`에 슬라이드 구조를 추가하고 HUD의 총 슬라이드 개수를 갱신합니다. 
3. **연결**: `script.js`에서 차트 초기화 로직을 추가합니다(필요 시).
4. **검증**: `data-step` 순서와 1300px 중앙 정렬 수직 축이 맞는지 확인합니다.


## 🛠️ 문제 해결 및 베스트 프랙티스

### 7.1 첫 슬라이드 애니메이션 누락 방지
- **현상**: 페이지 로드 후 첫 번째 슬라이드에서 `data-step` 요소들이 나타나지 않고 빈 화면으로 남는 현상. (다른 슬라이드로 갔다가 돌아와야 출력됨)
- **원인**: `Presentation` 클래스 초기화 시 `this.currentIndex = 0`으로 시작할 경우, 초기 `handleHash()`가 `goto(0)`를 호출할 때 "현재와 동일한 인덱스"로 판단하여 `triggerSteps()` 실행을 건너뛰기 때문입니다.
- **해결책**: 클래스 생성자(`constructor`)에서 `this.currentIndex = -1;`로 초기화하여 첫 번째 `goto(0)` 호출이 반드시 전체 로직을 수행하도록 보장합니다.

---