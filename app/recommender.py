from app.models import Bakery


def recommend(
    bakeries: list[Bakery],
    mood: str | None = None,
    purpose: str | None = None,
    price_range: str | None = None,
    parking: bool | None = None,
    custom_order: bool | None = None,
    max_distance: float | None = None,
    max_results: int = 3,
) -> list[Bakery]:
    # 1. 불리언/거리 필터링
    filtered = bakeries
    if parking is not None:
        filtered = [b for b in filtered if b.parking == parking]
    if custom_order is not None:
        filtered = [b for b in filtered if b.custom_order == custom_order]
    if max_distance is not None:
        filtered = [b for b in filtered if b.distance <= max_distance]

    # 2. 점수 계산
    scored: list[tuple[float, Bakery]] = []
    for bakery in filtered:
        score = bakery.rating * 0.5

        if mood and mood in bakery.mood:
            score += 2
        if purpose and purpose in bakery.purpose:
            score += 2
        if price_range and bakery.price_range == price_range:
            score += 1

        # 거리 보너스: 가까울수록 높은 점수
        if max_distance and max_distance > 0:
            score += max(0, (max_distance - bakery.distance) / max_distance)

        scored.append((score, bakery))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [bakery for _, bakery in scored[:max_results]]
