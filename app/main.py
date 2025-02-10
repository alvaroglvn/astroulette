from typing import Annotated, AsyncGenerator

from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.models import *
from app.config import AppSettings

from app.services.leonardo.img_request import PhoenixPayload, generate_image

from app.services.openai.prompter import character_creator
from app.services.openai.assistant import create_assistant

from app.db.database import create_db_tables, get_session
from app.db.queries import *

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


# Generate new character and add it to the database
@app.post("/generate_character")
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

            new_assistant = create_assistant(settings.openai_api_key, new_character)

            if image_url and new_assistant:
                # Add new character to database
                store_character(new_character, image_url, new_assistant.id, session)
                print("Character generation succesful!")

                return Response(
                    content="New character added to the database.", status_code=201
                )

        retries += 1
        print(f"Retry {retries} of {max_retries}...")
    return Response(
        content=f"Character generation failed after {max_retries} retries.",
        status_code=417,
    )


# Add character to the database manually
@app.post("/add_character")
async def add_character(
    character_data: NewCharacterRequest, session: SessionDep
) -> Response:
    """This endpoint allows to add a new character to the database manually, instead of automatically generated"""
    new_character = store_character(
        character_data.model_dump(), character_data.image_url, session
    )
    if new_character:
        return Response(
            content="New character manually added to the database.", status_code=201
        )
    return Response(content="Unable to add character to the database.", status_code=404)


# Delete character from the database
@app.delete("/delete_character/{profile_id}")
async def delete_character(profile_id: int, session: SessionDep) -> Response:

    success = delete_entry(profile_id, session)

    if success:
        return Response(content=f"Profile {profile_id} deleted", status_code=200)

    return Response(status_code=404, content=f"Profile {profile_id} not in database")


@app.post("/character_test")
async def test_character_creator():
    response = character_creator(settings.openai_api_key)
    print(type(response))
    print(response)
