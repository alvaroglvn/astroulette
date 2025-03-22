import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import db_dependency, settings_dependency
from app.services.openai.chat import ai_response
from app.db.db_crud import read_record, store_message, get_last_resp_id, fetch_thread
from app.db.db_models import User, CharacterProfile

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/chat-ui", response_class=HTMLResponse)
async def load_chat(request: Request):
    return templates.TemplateResponse(request=request, name="chat.html")


@router.websocket("/chat")
async def chat_with_character(
    websocket: WebSocket,
    session: db_dependency,
    settings: settings_dependency,
    user_id: int = 1,  # Hardcoded admin for now
    profile_id: int = 1,  # Hardcoded for now
):
    # Accept the WebSocket connection
    await websocket.accept()
    try:
        # Fetch thread, user and character details needed for context
        thread = await fetch_thread(session, user_id, profile_id)
        user = await read_record(session, User, user_id, "username")
        character = await read_record(session, CharacterProfile, profile_id)

        while True:
            # Receive a text message from the client
            user_message = await websocket.receive_text()

            # Store the user message in your database
            await store_message(
                session, thread.id, user_id, profile_id, "user", user_message
            )

            # Retrieve the last OpenAI response id, if any, for context
            last_response_id = await get_last_resp_id(session, thread.id)
            if not last_response_id:
                last_response_id = None

            # Get the streaming response from OpenAI using your custom logic
            response = await ai_response(
                settings.openai_api_key, user, character, user_message, last_response_id
            )

            # Initialize variables to capture the final response details
            openai_response_id = None
            content = ""
            role = ""
            created_at = None

            # Stream the response back to the client chunk by chunk
            async for chunk in response:
                if chunk.type == "response.output_text.delta":
                    await websocket.send_text(chunk.delta)
                elif chunk.type == "response.completed":
                    openai_response_id = chunk.response.id
                    content = chunk.response.output[0].content[0].text
                    role = chunk.response.output[0].role
                    created_at = chunk.response.created_at

            # After the stream completes, store the assistant's response if available
            if openai_response_id:
                await store_message(
                    session,
                    thread.id,
                    user_id,
                    profile_id,
                    role,
                    content,
                    created_at=created_at,
                    openai_response_id=openai_response_id,
                )

    except WebSocketDisconnect:
        # The client disconnected; you might want to perform cleanup here.
        pass
    except Exception as e:
        # Log the error if desired and close the WebSocket connection gracefully.
        logging.error(e)
        await websocket.close()
