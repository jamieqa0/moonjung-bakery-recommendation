from app.review_analyzer import extract_tags


class TestExtractTags:
    def test_extract_bread_tag(self):
        reviews = ["소금빵이 정말 맛있어요", "바게트가 훌륭해요"]
        tags = extract_tags(reviews)
        assert "빵맛집" in tags

    def test_extract_cake_tag(self):
        reviews = ["케이크가 너무 예뻐요", "생크림이 부드러워요"]
        tags = extract_tags(reviews)
        assert "케이크맛집" in tags

    def test_extract_multiple_tags(self):
        reviews = ["빵이 맛있고", "케이크도 훌륭해요", "가성비 좋아요"]
        tags = extract_tags(reviews)
        assert len(tags) >= 2

    def test_empty_reviews(self):
        tags = extract_tags([])
        assert tags == []

    def test_no_matching_keywords(self):
        reviews = ["그냥 그래요"]
        tags = extract_tags(reviews)
        assert tags == []

    def test_extract_cozy_tag(self):
        reviews = ["아늑하고 따뜻한 분위기예요"]
        tags = extract_tags(reviews)
        assert "아늑한" in tags

    def test_extract_value_tag(self):
        reviews = ["가성비가 최고예요", "가격 대비 만족"]
        tags = extract_tags(reviews)
        assert "가성비좋은" in tags

    def test_extract_gift_tag(self):
        reviews = ["선물용으로 포장해줘요", "예쁜 박스에 담아줘요"]
        tags = extract_tags(reviews)
        assert "선물하기좋은" in tags
