from fastapi import APIRouter

# main.py의 app을 직접 import하지 않고 router만 정의합니다.
# main.py가 이 router를 include_router()로 등록하는 구조라서 파일 간 의존성이 단순해집니다.
router = APIRouter()
@router.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
