from __future__ import annotations

# NOTE: kiwipiepy(형태소 분석기)는 Render 무료 플랜 메모리(512MB) 초과로 제거.
# 현재 키워드들은 한국어 특성상 원본 텍스트에 그대로 포함되어 있어
# 단순 부분 문자열 검색(kw in text)으로 거의 동일한 정확도를 유지한다.
# 예) "웨이팅이있어요" → "웨이팅" in "웨이팅이있어요" == True

KEYWORD_TAG_MAP: dict[str, list[str]] = {
    "아늑한": ["아늑", "따뜻", "포근"],
    "케이크맛집": ["케이크", "생크림", "시트", "레이어", "생일케이크"],
    "마카롱맛집": ["마카롱", "꼬끄"],
    "소금빵맛집": ["소금빵"],
    "쿠키맛집": ["쿠키", "타르트", "까눌레", "두쫀쿠"],
    "베이글맛집": ["베이글"],
    "가성비좋은": ["가성비", "저렴", "가격 대비"],
    "줄서는집": ["줄", "웨이팅", "대기", "오픈런", "조기마감", "품절"],
    "선물하기좋은": ["선물", "포장", "예쁜 박스"],
    "브런치맛집": ["브런치", "샌드위치", "토스트", "스콘"],
    "식사빵": ["발효", "통밀", "치아바타", "깜빠뉴", "바게트", "호밀", "담백", "식사"],
    "동네 단골": ["동네", "단골", "편안한", "매일"],
    "대형빵집": ["대형", "넓은", "쾌적", "주차편한", "2층", "대규모"],
    "친절한": ["친절"],
}


def extract_tags(reviews: list[str], min_reviews: int = 1) -> list[str]:
    """리뷰 목록에서 태그를 추출한다.

    Args:
        reviews: 방문자 리뷰 문자열 목록
        min_reviews: 태그가 붙으려면 키워드가 등장해야 하는 최소 리뷰 수 (기본 1).
                     값을 높이면 신뢰도 높은 태그만 남긴다 (빈도 가중치).
    """
    if not reviews:
        return []

    tags = []
    for tag, keywords in KEYWORD_TAG_MAP.items():
        match_count = sum(
            1 for raw in reviews
            if any(kw in raw for kw in keywords)
        )
        if match_count >= min_reviews:
            tags.append(tag)

    return tags


# mood/purpose → 태그 매핑 (리뷰 없는 빵집용 폴백)
_MOOD_TAG_MAP: dict[str, str] = {
    "아늑한": "아늑한",
    "편안한": "동네 단골",
    "감성적인": "선물하기좋은",
    "모던한": "모던한",
    "동네 단골": "동네 단골",
    "대형빵집": "대형빵집",
}

_PURPOSE_TAG_MAP: dict[str, str] = {
    "브런치": "브런치맛집",
    "선물": "선물하기좋은",
    "케이크": "케이크맛집",
    "식사빵": "식사빵",
}


def generate_fallback_tags(mood: list[str], purpose: list[str]) -> list[str]:
    """리뷰가 없을 때 mood/purpose에서 태그를 생성한다."""
    tags: list[str] = []
    for m in mood:
        if m in _MOOD_TAG_MAP and _MOOD_TAG_MAP[m] not in tags:
            tags.append(_MOOD_TAG_MAP[m])
    for p in purpose:
        if p in _PURPOSE_TAG_MAP and _PURPOSE_TAG_MAP[p] not in tags:
            tags.append(_PURPOSE_TAG_MAP[p])
    return tags
