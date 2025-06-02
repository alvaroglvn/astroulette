from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.config.session import db_dependency
from backend.db.db_crud import read_all_filtered, delete_record
from backend.db.db_models import Message, Thread
from backend.db.db_excepts import DatabaseError, TableNotFound

router = APIRouter()


@router.get("/thread/{thread_id}")
async def get_chat_history(session: db_dependency, thread_id: int) -> JSONResponse:
    try:
        messages = await read_all_filtered(session, Message, thread_id=thread_id)
        if not messages:
            return JSONResponse(content="No messages found", status_code=404)
        messages.sort(key=lambda m: m.created_at)
        chat_history = [
            {"role": message.role, "content": message.content} for message in messages
        ]

        return JSONResponse(content={"chat_history": chat_history}, status_code=200)
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.delete("/thread/{thread_id}")
async def delete_chat(session: db_dependency, thread_id: int) -> JSONResponse:
    try:
        await delete_record(session, Thread, thread_id)
        return JSONResponse(content="Thread deleted", status_code=200)
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)
