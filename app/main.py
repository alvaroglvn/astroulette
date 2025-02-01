from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://127.0.0.1:8000/", "http://localhost", "https://localhost"]
app.add_middleware(
    CORSMiddleware(
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
)


@app.get("/")
async def root() -> None:
    pass
