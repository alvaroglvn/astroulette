from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import openai

from app.dependencies import db_dependency

from app.db.db_models import CharacterProfile
from app.db.db_crud import read_record, fetch_thread, create_record

from app.services.openai.openai_models import message_mapper

router = APIRouter()
active_sessions = {}


@router.websocket("/chat/{profile_id}/{user_id}")
async def chat_endpoint(
    websocket: WebSocket,
    profile_id: int,
    user_id: int,
    session: db_dependency,
):
    await websocket.accept()

    # client = openai.AsyncClient(api_key=settings.openai_api_key)

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

    active_sessions[user_id] = {
        "previous_response_id": None,
        "thread_id": thread.id,
    }

    await websocket.send_text(f"System: {character.name} has joined the chat!")

    # Session tracking
    active_sessions[user_id] = {
        "previous_response_id": None,
        "thread_id": thread.id,
    }

    try:
        while True:
            user_message = await websocket.receive_text()

            # Store user message
            stored_user_message = message_mapper(
                thread.id,
                user_id,
                profile_id,
                "user",
                user_message,
            )
            await create_record(session, stored_user_message)

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

                # Accumulate AI response for storage
                ai_response = ""

                async for event in response:
                    if event.type == "text_delta":
                        ai_response += event.delta
                        await websocket.send_text(event.delta)
                    elif event.type == "text_done":
                        break

                # Store AI response
                stored_ai_message = message_mapper(
                    thread.id,
                    user_id,
                    profile_id,
                    "assistant",
                    ai_response,
                )
                await create_record(session, stored_ai_message)

                active_sessions[user_id][
                    "previous_response_id"
                ] = response.previous_response_id
    except WebSocketDisconnect:
        print("Client disconnected")
        active_sessions.pop(user_id, None)
