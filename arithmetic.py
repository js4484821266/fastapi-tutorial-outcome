from .main import app


@app.get("/{a}/plus/{b}")
async def deohagi(a: float, b: float):
    return {"Ans": a + b}


@app.get("{a}/minus/{b}")
async def ppaegi(a: float, b: float):
    return {"Ans": a - b}
