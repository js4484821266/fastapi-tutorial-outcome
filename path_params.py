from enum import Enum

from fastapi import APIRouter

# main.py의 app을 직접 import하지 않고 router만 정의합니다.
# main.py가 이 router를 include_router()로 등록하는 구조라서 파일 간 의존성이 단순해집니다.
router = APIRouter()


class ModelName(str, Enum):
    # Enum을 쓰면 model_name에 허용할 값을 alexnet, resnet, lenet으로 제한할 수 있습니다.
    # FastAPI 문서(/docs)에서도 가능한 값이 자동으로 표시됩니다.
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# main.py에서 path_params_router를 등록하므로 이 함수는 /models/{model_name} API가 됩니다.
# model_name: ModelName 타입 힌트 덕분에 FastAPI가 값 검증과 문서화를 자동 처리합니다.
@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}