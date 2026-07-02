from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


################################################################################
@app.get("/")
async def default():
    return {"message": "hi there"}


import random
import socket

import uvicorn


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
