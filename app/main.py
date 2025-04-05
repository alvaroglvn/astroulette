from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_init import init_db
from app.routes.rt_users import router as users
from app.routes.rt_characters import router as characters
from app.routes.chat_websocket import router as chat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(characters)
app.include_router(users)
app.include_router(chat)
