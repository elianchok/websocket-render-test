import asyncio
import json
import zlib
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "ok", "test": "websocket compression"}

# Same payload sent in plain text or as zlib-compressed binary.
payload = json.dumps({
    "type": "arena_snapshot",
    "fighters": [
        {"id": i, "x": i * 1.25, "y": i * 0.75, "health": 100,
         "color": "blue", "state": "moving", "effects": ["glow", "trail"]}
        for i in range(125)
    ]
}, separators=(",", ":")).encode("utf-8")
compressed = zlib.compress(payload, level=6)

@app.websocket("/ws")
async def websocket_plain(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_text(payload.decode("utf-8"))
            await asyncio.sleep(0.1)
    except Exception:
        pass

@app.websocket("/ws-compressed")
async def websocket_compressed(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_bytes(compressed)
            await asyncio.sleep(0.1)
    except Exception:
        pass
