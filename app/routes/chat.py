from fastapi import APIRouter, WebSocket
from fastapi.responses import JSONResponse
from app.dependencies import db_dependency, settings_dependency
from app.services.openai.chat import ai_response

from app.db.db_crud import read_record, store_message, get_last_resp_id

from app.db.db_models import User, CharacterProfile

router = APIRouter()


@router.websocket("/chat/{user_id}/{character_id}")
async def chat_with_character(
    websocket: WebSocket,
    session: db_dependency,
    settings: settings_dependency,
    thread_id: 1,  # Hardcoded for now
    user_id=1,  # Hardcoded admin for now
    profile_id=10,  # Hardcoded for now
):

    user = await read_record(session, User, user_id, "username")
    character = await read_record(session, CharacterProfile, profile_id)

    await websocket.accept()

    while True:
        user_message = await websocket.receive_text()

        # Store user message
        await store_message(
            session, thread_id, user_id, profile_id, "user", user_message
        )

        # Get the last response id
        last_response_id = await get_last_resp_id(session, thread_id)

        response = await ai_response(
            settings.openai_api_key, user, character, user_message, last_response_id
        )

        # Init variables for message storage
        openai_response_id: str
        content: str
        role: str
        created_at: int

        # Stream response back
        async for chunk in response:
            if response.type == "response.output_text.delta":
                await websocket.send_text(chunk.delta)
            elif response.type == "response.completed":
                openai_response_id = chunk.response.id
                content = chunk.response.output[0].content[0].text
                role = chunk.response.output[0].role
                created_at = chunk.response.created_at

        # Store ai response
        await store_message(
            session,
            openai_response_id,
            thread_id,
            user_id,
            profile_id,
            role,
            content,
            created_at,
        )
