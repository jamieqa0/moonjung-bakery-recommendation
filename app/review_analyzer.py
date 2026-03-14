KEYWORD_TAG_MAP: dict[str, list[str]] = {
    "아늑한": ["아늑", "따뜻", "포근"],
    "빵맛집": ["빵", "식빵", "바게트", "크루아상", "소금빵"],
    "케이크맛집": ["케이크", "생크림", "시트", "레이어"],
    "마카롱맛집": ["마카롱", "꼬끄"],
    "가성비좋은": ["가성비", "저렴", "가격 대비"],
    "줄서는집": ["줄", "웨이팅", "대기"],
    "선물하기좋은": ["선물", "포장", "예쁜 박스"],
    "브런치맛집": ["브런치", "샌드위치", "토스트", "스콘"],
    "식사빵": ["발효", "통밀", "치아바타", "깜빠뉴", "담백", "식사"],
    "동네 단골": ["동네", "단골", "편안한", "매일"],
    "대형빵집": ["대형", "넓은", "쾌적", "주차편한", "2층", "대규모"],
}


def extract_tags(reviews: list[str]) -> list[str]:
    if not reviews:
        return []

    combined = " ".join(reviews)
    tags = []

    for tag, keywords in KEYWORD_TAG_MAP.items():
        if any(kw in combined for kw in keywords):
            tags.append(tag)

    return tags


# mood/purpose → 태그 매핑 (리뷰 없는 빵집용 폴백)
_MOOD_TAG_MAP: dict[str, str] = {
    "아늑한": "아늑한",
    "편안한": "동네 단골",
}

_PURPOSE_TAG_MAP: dict[str, str] = {
    "빵구경": "빵맛집",
    "브런치": "브런치맛집",
    "선물": "선물하기좋은",
    "케이크": "케이크맛집",
    "동네 단골": "동네 단골",
    "대형빵집": "대형빵집",
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
