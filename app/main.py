from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_setup import init_db
from app.routes.character_creation import router as characters
from app.routes.chat import router as chat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(characters)
app.include_router(chat)
