from fastapi import APIRouter

# APIRouter는 여러 API 경로를 묶어 두는 작은 라우팅 객체입니다.
# 여기서 app을 직접 만들거나 main.py의 app을 import하지 않고 router만 만들면,
# 이 파일은 독립적으로 라우트 정의만 담당하게 됩니다.
router = APIRouter()


# main.py에서 app.include_router(arithmetic_router)를 호출하기 때문에
# 이 경로는 최종적으로 FastAPI 앱의 /{a}/plus/{b} 엔드포인트가 됩니다.
@router.get("/{a}/plus/{b}")
async def deohagi(a: float, b: float):
    return {"Ans": a + b}


# 앞에 /를 붙여야 FastAPI가 올바른 절대 경로로 인식합니다.
# 기존의 "{a}/minus/{b}"처럼 시작 슬래시가 없으면 경로 정의가 잘못될 수 있습니다.
@router.get("/{a}/minus/{b}")
async def ppaegi(a: float, b: float):
    return {"Ans": a - b}