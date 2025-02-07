from typing import Annotated, AsyncGenerator

from fastapi import FastAPI, Depends, Response, status
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.models import *
from app.config import AppSettings
from app.services.leonardo.img_request import PhoenixPayload, generate_image
from app.services.openai.prompter import character_creator
from app.db.database import create_db_tables, get_session
from app.db.queries import store_character

# Load app settings
settings = AppSettings()


# Load database and its dependency
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    create_db_tables()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate")
async def generate_character(
    session: SessionDep,
    max_retries: int = 3,
) -> Response:

    retries = 0
    while retries < max_retries:
        new_character = character_creator(settings.openai_api_key)

        if new_character:

            payload = PhoenixPayload(
                prompt=new_character["image_prompt"],
                width=800,
                height=800,
                num_images=1,
                alchemy=False,
                contrast=4,
                enhancePrompt=False,
                styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd",  # Vibrant
                ultra=False,
            )
            image_url = await generate_image(settings.leonardo_api_key, payload)

            if image_url:
                # Add new character to database
                store_character(new_character, image_url, session)
                print("Character generation succesful!")

                return Response(
                    content="New character added to the database", status_code=201
                )

        retries += 1
        print(f"Retry {retries} of {max_retries}...")
    return Response(
        content=f"Character generation failed after {max_retries} retries.",
        status_code=417,
    )
