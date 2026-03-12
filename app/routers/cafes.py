from fastapi import APIRouter, HTTPException

from app.data import BAKERIES

router = APIRouter(prefix="/api/bakeries", tags=["bakeries"])


@router.get("/")
def get_all_bakeries():
    return BAKERIES


@router.get("/{bakery_id}")
def get_bakery(bakery_id: int):
    for bakery in BAKERIES:
        if bakery.id == bakery_id:
            return bakery
    raise HTTPException(status_code=404, detail="베이커리를 찾을 수 없습니다")
