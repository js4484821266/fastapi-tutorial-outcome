from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class ExperimentCreate(BaseModel):
    name: str
    target_count: int


experiments: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/experiments", status_code=201)
def create_experiment(data: ExperimentCreate):
    if data.target_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="target_count must be greater than 0",
        )

    experiment = {
        "id": len(experiments) + 1,
        "name": data.name,
        "target_count": data.target_count,
    }

    experiments.append(experiment)
    return experiment


@app.get("/experiments")
def list_experiments():
    return experiments


@app.get("/experiments/{experiment_id}")
def get_experiment(experiment_id: int):
    for experiment in experiments:
        if experiment["id"] == experiment_id:
            return experiment

    raise HTTPException(
        status_code=404,
        detail="experiment not found",
    )


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
