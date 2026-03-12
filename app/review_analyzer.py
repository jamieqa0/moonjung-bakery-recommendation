KEYWORD_TAG_MAP: dict[str, list[str]] = {
    "아늑한": ["아늑", "따뜻", "포근"],
    "빵맛집": ["빵", "식빵", "바게트", "크루아상", "소금빵"],
    "케이크맛집": ["케이크", "생크림", "시트", "레이어"],
    "마카롱맛집": ["마카롱", "꼬끄"],
    "가성비좋은": ["가성비", "저렴", "가격 대비"],
    "줄서는집": ["줄", "웨이팅", "대기"],
    "선물하기좋은": ["선물", "포장", "예쁜 박스"],
    "브런치맛집": ["브런치", "샌드위치", "토스트", "스콘"],
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
