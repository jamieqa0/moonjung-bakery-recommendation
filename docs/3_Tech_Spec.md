# 문빵 스테이션 — 기술 명세서

---

## 1. 기술 스택

### 백엔드

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic (데이터 모델 검증)
- python-dotenv (환경변수)

### 프론트엔드

- Jinja2 템플릿
- HTML / CSS (CSS Grid, CSS 변수 기반 디자인 시스템)
- 카카오맵 JS SDK (지도 렌더링)
- tsparticles (별 파티클 배경 효과, CDN)

### 테스트

- pytest

---

## 2. 시스템 아키텍처

```
클라이언트 (브라우저)
    │
    ├─ HTML 라우트 ──→ Jinja2 템플릿 렌더링
    │                     │
    │                     ├─ 카카오맵 JS SDK (비동기 로딩)
    │                     └─ tsparticles (CDN)
    │
    └─ JSON API ─────→ FastAPI 라우터
                          │
                          ▼
                   추천 엔진 (recommender.py)
                          │
                          ▼
                   인메모리 시드 데이터 (data.py)
```

---

## 3. 프로젝트 구조

```
app/
├── main.py            ← FastAPI 앱 엔트리포인트, HTML 라우트, .env 로딩
├── models.py          ← Pydantic 모델 (Bakery, RecommendRequest, RecommendResponse)
├── data.py            ← 시드 데이터 10곳, 좌표, 일러스트 매핑, 공공데이터 로더(비활성)
├── recommender.py     ← 추천 로직 (필터링 → 점수 계산 → 정렬)
├── review_analyzer.py ← 리뷰 키워드 → 태그 매핑
├── sensory.py         ← 감각 기반 추천 매핑 (식감×맛→purpose, 분위기→mood)
└── routers/
    ├── cafes.py       ← GET /api/bakeries, GET /api/bakeries/{id}
    └── recommend.py   ← POST /api/recommend

templates/
├── base.html          ← 레이아웃 셸 (헤더, 네비, 푸터, tsparticles)
├── index.html         ← 2컬럼: 소개+히어로 / 튜토리얼+칩 선택 폼
├── sensory.html       ← 2컬럼: 소개 / 3단계 이진 질문 폼
├── results.html       ← 3영역 그리드: 제목 + 카카오맵(sticky) + 카드 리스트
└── 404.html           ← 커스텀 404 페이지

static/
├── style.css          ← 앰버/크러스트 색상 팔레트, CSS Grid, 칩 그룹
├── icons/             ← 우주 테마 SVG 아이콘 세트
├── illust/            ← 빵 종류별 SVG 일러스트 (croissant/cake/loaf/scone/macaron)
├── hero-alien.svg     ← 히어로 일러스트 (빵을 든 우주인)
└── favicon.svg        ← SVG 파비콘

tests/
├── conftest.py        ← 공통 fixture (client, sample_cafes)
├── test_models.py     ← 모델 유효성
├── test_recommender.py← 추천 로직 단위 테스트
├── test_review_analyzer.py ← 리뷰 분석 단위 테스트
├── test_sensory.py    ← 감각 매핑 단위 테스트
├── test_data.py       ← 데이터 무결성 (좌표, ID 유일성, haversine 등)
└── test_api.py        ← API + HTML 통합 테스트
```

---

## 4. API 설계

### HTML 라우트

| 메서드 | 경로 | 용도 |
|--------|------|------|
| GET | `/` | 메인 페이지 — 칩 기반 조건 선택 폼 |
| POST | `/recommend` | 폼 제출 → 카카오맵 + 카드 결과 페이지 |
| GET | `/sensory` | 감각 기반 추천 폼 |
| POST | `/sensory` | 감각 폼 제출 → 결과 페이지 |

### JSON API

#### 베이커리 목록 조회

```
GET /api/bakeries

응답:
[
  {
    "id": 1,
    "name": "더 브레드 레지던스",
    "address": "서울 송파구 문정로 19",
    "mood": ["모던한", "감성적인"],
    "purpose": ["빵구경", "브런치"],
    "signature_menu": "소금빵",
    "price_range": "일반",
    "rating": 4.6,
    "description": "문정역 바로 앞, 갓 구운 빵 향이 퍼지는 동네 명소",
    "parking": false,
    "custom_order": false,
    "distance": 0.16,
    "lat": 37.4863,
    "lon": 127.1247,
    "flavor_profile": "겉은 바삭, 속에서 짭짤한 버터가 흘러나온다...",
    "image_url": "/static/illust/croissant.svg",
    "reviews": ["소금빵이 진짜 맛있어요...", ...],
    "tags": ["빵맛집", "줄서는집", ...]
  },
  ...
]
```

#### 베이커리 상세 조회

```
GET /api/bakeries/{id}

200: Bakery 객체 (위와 동일 구조)
404: {"detail": "Bakery not found"}
```

#### 추천 요청

```
POST /api/recommend

요청:
{
  "mood": "아늑한",
  "purpose": "브런치",
  "price_range": "일반",
  "parking": true,
  "custom_order": false,
  "max_distance": 1.0
}
(모든 필드 선택사항)

응답:
{
  "bakeries": [ ... ],
  "total": 5
}
```

---

## 5. 데이터 모델

```python
class Bakery(BaseModel):
    id: int
    name: str
    address: str
    mood: list[str]           # ["아늑한", "편안한"] 등 복수
    purpose: list[str]        # ["브런치", "선물"] 등 복수
    signature_menu: str
    price_range: str          # "일반" | "프리미엄"
    rating: float
    description: str
    parking: bool = False
    custom_order: bool = False
    distance: float = 0.0    # 문정역까지 km
    lat: float = 0.0         # WGS84 위도
    lon: float = 0.0         # WGS84 경도
    flavor_profile: str = "" # 맛·식감 감각 묘사
    image_url: str = ""      # 빵 일러스트 SVG 경로
    reviews: list[str] = []
    tags: list[str] = []     # review_analyzer가 자동 생성

class RecommendRequest(BaseModel):
    mood: str | None = None
    purpose: str | None = None
    price_range: str | None = None
    parking: bool | None = None
    custom_order: bool | None = None
    max_distance: float | None = None

class RecommendResponse(BaseModel):
    bakeries: list[Bakery]
    total: int
```

---

## 6. 추천 엔진

### 필터링 단계

- `parking is not None` → `bakery.parking == parking` 정확 일치
- `custom_order is not None` → `bakery.custom_order == custom_order` 정확 일치
- `max_distance is not None` → `bakery.distance <= max_distance` 반경 필터

### 점수 계산

```
score =
  rating × 0.5                                        (기본 점수)
+ (mood in bakery.mood ? 2 : 0)                       (분위기 일치)
+ (purpose in bakery.purpose ? 2 : 0)                  (목적 일치)
+ (price_range == bakery.price_range ? 1 : 0)          (가격대 일치)
+ ((max_distance - distance) / max_distance) × 3       (거리 보너스)
+ random(0 ~ 1.5)                                      (랜덤 다양화)
```

### 정렬 및 반환

- 점수 내림차순 정렬
- HTML 라우트: 상위 3개 반환
- API: 상위 5개 반환 (기본값)

---

## 7. 리뷰 태그 추출

키워드 → 태그 매핑 (review_analyzer.py)

| 태그 | 키워드 |
|------|--------|
| 아늑한 | 아늑, 따뜻, 포근 |
| 빵맛집 | 빵, 식빵, 바게트, 크루아상, 소금빵 |
| 케이크맛집 | 케이크, 생크림, 시트, 레이어 |
| 마카롱맛집 | 마카롱, 꼬끄 |
| 가성비좋은 | 가성비, 저렴, 가격 대비 |
| 줄서는집 | 줄, 웨이팅, 대기 |
| 선물하기좋은 | 선물, 포장, 예쁜 박스 |
| 브런치맛집 | 브런치, 샌드위치, 토스트, 스콘 |

---

## 8. 감각 기반 추천 매핑

### 식감 × 맛 → purpose

| 식감 | 맛 | purpose |
|------|-----|---------|
| 바삭 | 달콤 | 빵구경 |
| 바삭 | 고소 | 브런치 |
| 부드러움 | 달콤 | 케이크 |
| 부드러움 | 고소 | 브런치 |

### 분위기 → mood

| 분위기 | mood |
|--------|------|
| 혼자 | 아늑한 |
| 여럿 | 편안한 |

---

## 9. 외부 연동

### 카카오맵 JS SDK

- `KAKAO_JS_KEY` 환경변수 필요 (없으면 지도 영역 미표시)
- `autoload=false` + `kakao.maps.load()` 콜백 패턴으로 비동기 로딩
- 문정역 기준 마커 + 베이커리 마커 + 인포윈도우
- SDK 실패 시 폴백 메시지 표시

### 일러스트 자동 매핑

- `_get_illust_url()` 함수가 대표 메뉴 키워드로 SVG 경로 결정
- croissant / cake / scone / macaron / loaf 5종

---

## 10. 성능 목표

- 추천 응답 시간: < 100ms (인메모리 데이터 기반)

---

## 11. 테스트 전략

pytest 기반 TDD. 외부 의존성 없이 독립 실행.

| 테스트 파일 | 대상 |
|------------|------|
| test_models.py | 모델 생성, 유효성 검증, Pydantic 에러 |
| test_recommender.py | 필터링(mood/purpose/price/parking/custom_order/distance), 점수 계산 |
| test_review_analyzer.py | 태그 추출, 복수 태그, 빈 리뷰, 미매칭 |
| test_sensory.py | 식감×맛 매핑, 분위기 매핑 |
| test_data.py | 좌표, 리뷰, 태그, ID 유일성, haversine, TM→WGS84, CSV 로더 |
| test_api.py | API 엔드포인트 + HTML 페이지 통합 테스트 |
