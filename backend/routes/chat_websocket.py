import logging
import traceback
from typing import List, Any, Dict
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from fastapi.responses import JSONResponse

from backend.config.settings import settings_dependency
from backend.config.session import db_dependency
from backend.services.openai.chat import ai_response
from backend.db.db_models import User, Character, Thread, Message
from backend.db.db_crud import (
    read_record,
    read_field,
    read_all_filtered,
    store_message,
    get_last_resp_id,
)

router = APIRouter()


@router.websocket("/chat/{thread_id}")
async def chat_with_character(
    websocket: WebSocket,
    session: db_dependency,
    settings: settings_dependency,
    thread_id: int,
) -> None:

    # Accept the WebSocket connection
    await websocket.accept()
    logging.info(f"WebSocket connection established for thread {thread_id}")

    try:
        # Load thread and validate thread
        thread = await read_record(session, Thread, thread_id)
        assert thread is not None, "No chat thread found"
        assert isinstance(thread, Thread), "Thread object is incorrect"
        assert isinstance(thread.id, int), "Thread id is not an int"

        while True:
            # Receive a text message from the client
            user_message = await websocket.receive_text()

            # Store the user message in your database
            await store_message(session, thread.id, "user", user_message)

            # Retrieve the last OpenAI response id, if any, for context
            last_response_id = await get_last_resp_id(session, thread.id)
            if last_response_id:
                assert isinstance(
                    last_response_id, str
                ), "Last response id is not an int"

            # Get the streaming response from OpenAI using your custom logic
            username = await read_field(session, User, thread.user_id, "username")
            assert isinstance(username, str)
            character = await read_record(session, Character, thread.character_id)
            assert character is not None
            assert isinstance(character, Character)

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
        logging.info("WebSocket disconnected")
    except AssertionError as e:
        logging.error(f"Assertion error: {e}")
        traceback.print_exc()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        traceback.print_exc()
    finally:
        if websocket.client_state.name == "CONNECTED":
            await websocket.close()


@router.get("/chat/history/{thread_id}")
async def get_chat_history(
    session: db_dependency,
    thread_id: int,
) -> JSONResponse:

    try:
        messages = await read_all_filtered(session, Message, thread_id=thread_id)

        if not messages:
            return JSONResponse(content=[], status_code=200)

        assert isinstance(messages, List)

        history: List[Dict[str, Any]] = [
            {
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in sorted(messages, key=lambda x: x.created_at)
        ]
        assert isinstance(history, List)
        return JSONResponse(content=history, status_code=200)
    except (AssertionError, Exception) as e:
        logging.error(f"Assertion error: {e}")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
