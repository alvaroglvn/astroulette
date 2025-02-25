from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.db_setup import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
