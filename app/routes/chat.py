from typing import Annotated
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import openai

from app.config import AppSettings
from app.dependencies import *
from app.db.db_crud import read_record

router = APIRouter()

openai_key = AppSettings().openai_api_key
client = openai.AsyncClient(api_key=openai_key)


@router.websocket("/chat")
async def chat_endpoint(
    websocket: WebSocket,
    session: db_dependency,
    settings: Annotated[AppSettings, Depends(settings_dependency)],
):
    await websocket.accept()

    # Load character
    character = await read_record()
    await websocket.send_text("Connected to chat")

    try:
        while True:
            user_message = await websocket.receive_text()

            async with client.response.create(
                model="gpt-4o", input=user_message, stream=True
            ) as response:

                async for event in response:
                    if event.type == "text_delta":
                        await websocket.send_text(event.delta)
                    elif event.type == "text_done":
                        break
    except WebSocketDisconnect:
        print("Client disconnected")
