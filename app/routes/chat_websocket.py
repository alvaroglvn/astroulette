import logging
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config.settings import settings_dependency
from app.config.session import db_dependency
from app.services.auth import valid_user_dependency
from app.chat_builder import chat_builder
from app.services.openai.chat import ai_response
from app.db.db_models import User, Character
from app.db.db_crud import (
    read_record,
    read_field,
    store_message,
    get_last_resp_id,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/chat-ui", response_class=HTMLResponse)
async def load_chat(
    request: Request,
    session: db_dependency,
    profile_id: int = 1,
) -> HTMLResponse:
    character = await read_record(session, Character, profile_id)
    return templates.TemplateResponse(
        request=request, name="chat.html", context={"character": character}
    )


@router.websocket("/chat")
async def chat_with_character(
    websocket: WebSocket,
    session: db_dependency,
    settings: settings_dependency,
    user: valid_user_dependency,
) -> None:
    # Build the chat thread for the specific user
    thread = await chat_builder(session, settings, user)
    # Accept the WebSocket connection
    await websocket.accept()
    try:
        while True:
            # Receive a text message from the client
            user_message = await websocket.receive_text()

            # Store the user message in your database
            if thread is None:
                raise ValueError("Thread is None")
            if thread.id is not int:
                raise ValueError("Thread ID is not an integer")
            await store_message(session, thread.id, "user", user_message)

            # Retrieve the last OpenAI response id, if any, for context
            last_response_id = await get_last_resp_id(session, thread.id)
            if not last_response_id:
                last_response_id = None

            # Get the streaming response from OpenAI using your custom logic
            username = await read_field(session, User, thread.user_id, "username")
            if username is not str:
                raise ValueError("Username must be a string")
            character = await read_record(session, Character, thread.character_id)
            if character is None:
                raise ValueError("Character must be a Character object")

            response = await ai_response(
                settings.openai_api_key,
                username,
                character,
                user_message,
                last_response_id,
            )

            # Initialize variables to capture the final response details
            openai_response_id = None
            content: str = ""
            role: str = ""
            created_at: int = 0

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
                    role,
                    content,
                    openai_response_id=openai_response_id,
                    created_at=created_at,
                )

    except WebSocketDisconnect:
        # The client disconnected; you might want to perform cleanup here.
        pass
    except Exception as e:
        # Log the error if desired and close the WebSocket connection gracefully.
        logging.error(e)
        await websocket.close()
