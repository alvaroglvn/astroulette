from typing import Annotated, AsyncGenerator, Generator

from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.db.db import DB
from app.db.db_models import *

from app.config import AppSettings

from app.services.leonardo.img_request import PhoenixPayload, generate_image

from app.services.openai.character_gen import character_generator
from app.services.openai.assistant_gen import create_assistant


# Load app settings
settings = AppSettings()

# Load database
db = DB("app/db/alien_talk.sqlite")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """FastAPI lifespan event allows the db to remain available throughout the app lifecycle"""
    yield


# Load app
app = FastAPI(lifespan=lifespan)


# Load db dependency
def get_session() -> Generator:
    with Session(db.engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Origins
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Load middleware
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
        try:

            # Generate new character
            character_gen = character_generator(settings.openai_api_key)

            if character_gen:
                # Build and store character profile
                character_profile = CharacterProfile(
                    name=character_gen.character_profile.name,
                    planet_name=character_gen.character_profile.planet_name,
                    planet_description=character_gen.character_profile.planet_description,
                    personality_traits=character_gen.character_profile.personality_traits,
                    speech_style=character_gen.character_profile.speech_style,
                    quirks=character_gen.character_profile.quirks,
                )
                db.store_entry(character_profile)
                print(f"{character_profile.name} stored in db.")

                # Build and store character's assistant
                assistant_gen = create_assistant(settings.openai_api_key, character_gen)

                if assistant_gen:
                    assistant = Assistant(
                        assistant_id=assistant_gen.id,
                        created_at=assistant_gen.created_at,
                        name=assistant_gen.name,
                        model=assistant_gen.model,
                        instructions=assistant_gen.instructions,
                        temperature=assistant_gen.temperature,
                    )
                    db.store_entry(assistant)
                    print(f"{assistant.name} added to db.")
                else:
                    raise SystemError(
                        f"Unable to create new assistant for    {character_profile.name}"
                    )

                # Generate character's portrait
                payload = PhoenixPayload(
                    prompt=character_gen["image_prompt"],
                    width=800,
                    height=800,
                    num_images=1,
                    alchemy=False,
                    contrast=4,
                    enhancePrompt=False,
                    styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd",  #    Vibrant
                    ultra=False,
                )
                image_url = await generate_image(settings.leonardo_api_key, payload)

                # Create and store character data
                character_data = CharacterData(
                    image_prompt=character_gen.image_prompt,
                    image_url=image_url,
                    assistant_id=assistant.assistant_id,
                    profile_id=character_profile.profile_id,
                )
                db.store_entry(character_data)
                print(f"Character data for {character_profile.name} stored  in db.")

                return Response(
                    content="New character generated successfully!", status_code=201
                )
        except Exception as e:
            retries += 1
            print(f"Error {e}. Retrying: {retries} of {max_retries}...")

    return Response(content="Unable to generate new character", status_code=500)


# # Add character to the database manually
# @app.post("/add_character")
# async def add_character(
#     character_data: NewCharacterRequest, session: SessionDep
# ) -> Response:
#     """This endpoint allows to add a new character to the database manually, instead of automatically generated"""
#     new_character = store_character(
#         character_data.model_dump(), character_data.image_url, session
#     )
#     if new_character:
#         return Response(
#             content="New character manually added to the database.", status_code=201
#         )
#     return Response(content="Unable to add character to the database.", status_code=404)


# # Delete character from the database
# @app.delete("/delete_character/{profile_id}")
# async def delete_character(profile_id: int, session: SessionDep) -> Response:

#     success = delete_entry(profile_id, session)

#     if success:
#         return Response(content=f"Profile {profile_id} deleted", status_code=200)

#     return Response(status_code=404, content=f"Profile {profile_id} not in database")


# @app.post("/character_test")
# async def test_character_creator():
#     response = character_creator(settings.openai_api_key)
#     print(type(response))
#     print(response)
