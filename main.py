import random
import socket

import uvicorn
from fastapi import FastAPI

# arithmetic.py와 path_params.py는 각각 자기 라우터(router)만 정의합니다.
# main.py가 그 라우터들을 가져와 앱에 등록하면, 하위 파일들이 main.py의 app을
# 다시 import하지 않아도 되므로 순환 import 문제를 피할 수 있습니다.
from query_params import router as qrr
from path_params import router as path_params_router
from arithmetic import router as arithmetic_router

app = FastAPI()

# include_router()는 다른 파일에 나누어 작성한 API 경로들을 현재 FastAPI 앱에 붙입니다.
# 아래 두 줄 때문에 arithmetic.py의 계산 API와 path_params.py의 모델 API가
# 모두 이 app의 라우트로 등록됩니다.
app.include_router(qrr)
app.include_router(path_params_router)
app.include_router(arithmetic_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_available_port(start=49152, end=65535):
    # 지정한 포트 범위 전체를 섞은 뒤 하나씩 bind를 시도합니다.
    # bind가 성공하면 현재 사용 중이 아닌 포트라는 뜻이므로 그 포트를 반환합니다.
    ports = list(range(start, end + 1))
    random.shuffle(ports)

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("localhost", port))
                return port
            except OSError:
                # 이미 사용 중인 포트라면 다음 포트를 계속 확인합니다.
                continue

    raise RuntimeError("No available port found")


if __name__ == "__main__":
    # python main.py로 직접 실행할 때만 서버를 시작합니다.
    # main.py를 다른 파일이나 테스트에서 import할 때는 서버가 자동 실행되지 않습니다.
    port = get_available_port()
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="localhost", port=port, reload=False)