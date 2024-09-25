from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.config import load_config
from app.listener import start_sse_listener
from app.utils import set_models
import asyncio

config = load_config()

def setup_routes(app: FastAPI):
    app.queue = asyncio.Queue()
    app.mount("/widget", StaticFiles(directory="widget", html=True), name="widget")

    @app.on_event("startup")
    async def startup_event():
        set_models()
        asyncio.create_task(start_sse_listener(app))

    async def event_generator():
        while True:
            event = await app.queue.get()
            yield f"event: Message\ndata: {event}\n\n"

    @app.get("/events")
    async def widget_events():
        return StreamingResponse(event_generator(), media_type="text/event-stream")