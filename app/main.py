from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db_setup import init_db
from app.routers.route_chars import router as chars_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(chars_router, prefix="/api/v1")
