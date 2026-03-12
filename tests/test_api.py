class TestBakeriesAPI:
    def test_get_all_bakeries(self, client):
        response = client.get("/api/bakeries")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_bakery_by_id(self, client):
        response = client.get("/api/bakeries/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1

    def test_get_bakery_not_found(self, client):
        response = client.get("/api/bakeries/9999")
        assert response.status_code == 404


class TestRecommendAPI:
    def test_recommend_no_filter(self, client):
        response = client.post("/api/recommend", json={})
        assert response.status_code == 200
        data = response.json()
        assert "bakeries" in data
        assert "total" in data

    def test_recommend_with_mood(self, client):
        response = client.post("/api/recommend", json={"mood": "아늑한"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["bakeries"]) > 0

    def test_recommend_with_purpose(self, client):
        response = client.post("/api/recommend", json={"purpose": "브런치"})
        assert response.status_code == 200

    def test_recommend_with_all_filters(self, client):
        response = client.post(
            "/api/recommend",
            json={"mood": "아늑한", "purpose": "브런치", "price_range": "중가"},
        )
        assert response.status_code == 200


class TestHTMLPages:
    def test_index_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "문정동" in response.text
