# 문정동 베이커리 추천 시스템 개발 계획

## 목표

사용자가 분위기·목적·가격대를 선택하면 리뷰 기반 특징 분석을 거쳐 **TOP 3 베이커리**를 추천하는 웹 서비스.

## 기술 스택

- Python, FastAPI, Jinja2
- pytest (TDD)
- 인메모리 데이터 (DB 없음, MVP)
- 배포: Render (무료 티어)

## 링크

- **GitHub**: https://github.com/jamieqa0/moonjung-bakery-recommendation

## 실행 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행 (http://localhost:8000)
uvicorn app.main:app --reload

# 테스트 전체 실행
python -m pytest tests/ -v
```

---

## 개발 단계

### Phase 1. 데이터 모델 정의

> 테스트: `tests/test_models.py`

- `Bakery` 모델 — id, name, address, mood, purpose, signature_menu, price_range, rating, description, parking, custom_order, distance, reviews, tags
- `RecommendRequest` 모델 — mood, purpose, price_range (모두 optional)
- `RecommendResponse` 모델 — bakeries(list), total(int)

TDD 사이클:
1. Bakery 필수 필드 누락 시 ValidationError 발생 테스트
2. reviews, tags 기본값 빈 리스트 테스트
3. RecommendRequest 빈 요청 / 부분 요청 테스트
4. 모델 구현

현재 상태: **완료**

---

### Phase 2. 리뷰 기반 베이커리 특징 분석

> 테스트: `tests/test_review_analyzer.py`

`review_analyzer.py`의 `extract_tags(reviews: list[str]) -> list[str]` 함수 구현.

키워드-태그 매핑 규칙:

| 태그 | 매칭 키워드 |
|------|------------|
| 아늑한 | 아늑, 따뜻, 포근 |
| 빵맛집 | 빵, 식빵, 바게트, 크루아상, 소금빵 |
| 케이크맛집 | 케이크, 생크림, 시트, 레이어 |
| 마카롱맛집 | 마카롱, 꼬끄 |
| 가성비좋은 | 가성비, 저렴, 가격 대비 |
| 줄서는집 | 줄, 웨이팅, 대기 |
| 선물하기좋은 | 선물, 포장, 예쁜 박스 |
| 브런치맛집 | 브런치, 샌드위치, 토스트, 스콘 |

TDD 사이클:
1. 빈 리뷰 → 빈 태그 테스트
2. 매칭 키워드 없는 리뷰 → 빈 태그 테스트
3. 각 태그별 추출 테스트 (빵맛집, 케이크맛집, 아늑한, 가성비좋은, 선물하기좋은)
4. 복수 태그 동시 추출 테스트
5. 구현

현재 상태: **완료**

---

### Phase 3. TOP 3 추천 로직

> 테스트: `tests/test_recommender.py`

`recommender.py`의 `recommend()` 함수 구현.

#### 필터링

1. `parking` (bool | None) — 주차 가능 필터. None이면 무시
2. `custom_order` (bool | None) — 주문 제작 케이크 필터. None이면 무시
3. `max_distance` (float | None) — 문정역 기준 반경(km) 필터. `distance <= max_distance`

#### 점수 계산 공식

```
score = rating × 0.5
      + (mood 일치 시 +2)
      + (purpose 일치 시 +2)
      + (price_range 일치 시 +1)
      + (거리 보너스: (max_distance - distance) / max_distance)
```

점수 내림차순 정렬 후 **상위 3개** 반환 (max_results 기본값 3).
조건 미입력 시 rating 순 정렬.

테스트 클래스:
- `TestRecommendBasicFilter` — 기본 필터 (mood, purpose, price_range, max_results)
- `TestParkingFilter` — 주차 가능 필터
- `TestCustomOrderFilter` — 주문 제작 케이크 필터
- `TestDistanceFilter` — 거리 필터 + 거리 보너스
- `TestScoreCalculation` — 점수 누적, 순위 변동 검증

현재 상태: **완료**

---

### Phase 4. 시드 데이터

> 파일: `app/data.py`

문정동 베이커리 8곳 하드코딩. 앱 시작 시 `extract_tags()`로 각 베이커리의 tags 자동 생성.

| # | 이름 | 가격대 | 주차 | 주문제작 |
|---|------|:----:|:----:|:------:|
| 1 | 파리바게뜨 문정법조타운점 | 중가 | O | X |
| 2 | 뚜레쥬르 문정역점 | 중가 | X | O |
| 3 | 밀도 문정점 | 고가 | X | X |
| 4 | 봄봄 베이커리 | 중가 | X | X |
| 5 | 르뱅 문정 | 고가 | O | X |
| 6 | 크루아상하우스 문정 | 중가 | X | X |
| 7 | 마리 케이크 문정 | 고가 | O | O |
| 8 | 땅콩베이커리 문정 | 저가 | X | X |

현재 상태: **완료**

---

### Phase 5. API 엔드포인트

> 테스트: `tests/test_api.py`

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/bakeries` | 전체 베이커리 목록 (JSON) |
| GET | `/api/bakeries/{id}` | 단일 베이커리 조회 (JSON, 404 처리) |
| POST | `/api/recommend` | 추천 요청 → TOP 3 반환 (JSON) |

현재 상태: **완료**

---

### Phase 6. 웹 프론트엔드 (Jinja2)

> 테스트: `tests/test_api.py::TestHTMLPages`

| 경로 | 템플릿 | 설명 |
|------|--------|------|
| GET `/` | index.html | 조건 선택 폼 (분위기/목적/가격대) |
| POST `/recommend` | results.html | TOP 3 베이커리 카드 리스트 |

현재 상태: **완료**

---

## 남은 작업

### Phase 7. 시드 데이터 보강

> 파일: `app/data.py`

- [ ] 8개 베이커리에 `distance` 실제 값 확인 및 보강

### Phase 8. API 계층에 새 필터 반영

> 테스트: `tests/test_api.py`

- [ ] `RecommendRequest`에 `parking`, `custom_order`, `max_distance` 필드 추가
- [ ] `routers/recommend.py`에서 새 파라미터를 `recommend()`에 전달
- [ ] HTML POST `/recommend` 라우트에서도 새 폼 필드 처리
- [ ] 새 필터 파라미터 API 통합 테스트 추가 (TDD)

### Phase 9. 프론트엔드 업데이트

> 파일: `templates/index.html`, `templates/results.html`

- [ ] `index.html` 폼에 주차/주문제작 체크박스, 거리 셀렉트 추가
- [ ] `results.html`에 주차/주문제작/거리 정보 표시
- [ ] `results.html`에 "TOP 3" 명시 표시

### Phase 10. 실제 베이커리 데이터 수집 (카카오맵 API)

> 하드코딩 시드 데이터 → 실제 문정동 베이커리 데이터로 교체

1. [ ] https://developers.kakao.com 에서 앱 등록 + **REST API 키** 발급
2. [ ] 카카오 로컬 API로 "문정동 베이커리/빵집" 검색 → 이름/주소/좌표 수집
3. [ ] 좌표로 문정역(37.4857, 127.1264) 기준 거리(km) 계산
4. [ ] 리뷰 크롤링으로 리뷰 텍스트 보충 (카카오맵 or 네이버 지도)
5. [ ] 수집 데이터를 `app/data.py` 형식으로 변환

### 선택 (향후 확장)

- [ ] SQLite + SQLAlchemy로 데이터 영속화
- [ ] 베이커리 상세 페이지 (`/bakery/{id}`)
- [ ] 카카오맵 API 연동 (지도에 베이커리 위치 표시)
- [ ] 사용자 리뷰 등록 기능 → tags 실시간 재계산
- [ ] 키워드 가중치 도입 (빈도 기반 태그 신뢰도)
- [ ] 테스트 커버리지 측정 (`pytest-cov`)
