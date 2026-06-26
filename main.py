import random
import socket

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_available_port(start=49152, end=65535):
    ports = list(range(start, end + 1))
    random.shuffle(ports)

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue

    raise RuntimeError("No available port found")


if __name__ == "__main__":
    port = get_available_port()
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)