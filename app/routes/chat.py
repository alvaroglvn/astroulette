from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import openai

from app.dependencies import db_dependency, settings_dependency

from app.db.db_models import CharacterProfile
from app.db.db_crud import read_record, fetch_thread

router = APIRouter()
active_sessions = {}


@router.websocket("/chat/{character_id}/{user_id}")
async def chat_endpoint(
    websocket: WebSocket,
    profile_id: int,
    user_id: int,
    session: db_dependency,
    settings: settings_dependency,
):
    await websocket.accept()

    client = openai.AsyncClient(api_key=settings.openai_api_key)

    # Load character
    character = await read_record(
        session,
        CharacterProfile,
        profile_id,
    )

    if not character:
        await websocket.send_text("Character not found")
        await websocket.close()
        return

    # Load thread
    thread = await fetch_thread(session, user_id, profile_id)

    await websocket.send_text(f"System: {character.name} has joined the chat!")

    active_sessions[user_id] = {"previous_response_id": None}

    try:
        while True:
            user_message = await websocket.receive_text()

            # Get last response for this user, if any
            previous_response_id = active_sessions[user_id].get("previous_response_id")

            async with client.response.create(
                model="gpt-4o",
                instructions=f"You are {character.name}, an alien from the planet {character.planet_name}. You are {character.personality_traits}. You speak in a {character.speech_style} manner. You have the following quirks: {character.quirks}.",
                max_output_tokens=500,
                input=user_message,
                previous_response_id=previous_response_id,
                store=True,
                stream=True,
                temperature=1.0,
                user=user_id,
            ) as response:

                async for event in response:
                    if event.type == "text_delta":
                        await websocket.send_text(event.delta)
                    elif event.type == "text_done":
                        break

                active_sessions[user_id][
                    "previous_response_id"
                ] = response.previous_response_id
    except WebSocketDisconnect:
        print("Client disconnected")
        active_sessions.pop(user_id, None)
