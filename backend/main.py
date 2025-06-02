from typing import AsyncGenerator, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.db.db_init import init_db
from backend.routes.rt_users import router as users
from backend.routes.rt_characters import router as characters
from backend.routes.chat_websocket import router as chat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://astroulette.fly.dev",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters)
app.include_router(users)
app.include_router(chat)


@app.get("/")
async def root():
    return {"message": "Astroulette API is running!"}
