import asyncio
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "ok", "test": "websocket permessage-deflate"}

@app.websocket("/ws")
async def websocket_test(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_text("A" * 12000)
            await asyncio.sleep(0.1)
    except Exception:
        pass
