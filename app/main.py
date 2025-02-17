from typing import Annotated, AsyncGenerator, Generator
import json

from fastapi import FastAPI, Depends, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.db.db import DB
from app.db.db_models import *

from app.config import AppSettings
from app.models import *

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
    background_tasks: BackgroundTasks,
) -> Response:

    retries = 0
    max_retries = 3
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
                        f"Unable to create new assistant for        {character_profile.name}"
                    )

                # Create and store character data
                character_data = CharacterData(
                    image_prompt=character_gen.image_prompt,
                    assistant_id=assistant.assistant_id,
                    profile_id=character_profile.profile_id,
                )
                db.store_entry(character_data)
                print(f"Character data for {character_profile.name}  stored in db.")

                # Queue image generation in the background
                background_tasks.add_task(
                    character_portrait, character_data.character_id
                )

                return Response(
                    content="New character generated successfully!", status_code=201
                )
        except Exception as e:
            retries += 1
            print(f"Error {e}. Retrying: {retries} of {max_retries}...")

    return Response(content="Unable to generate new character", status_code=500)


async def character_portrait(character_id: int) -> Response:
    # Load character
    character = db.read_from_db(CharacterData, "character_id", character_id)

    # Generate character's portrait
    payload = PhoenixPayload(
        prompt=character.image_prompt,
        width=800,
        height=800,
        num_images=1,
        alchemy=False,
        contrast=4,
        enhancePrompt=False,
        styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84",  #    Vibrant
        ultra=False,
    )
    image_url = await generate_image(settings.leonardo_api_key, payload)

    # Update character with image url
    db.update_db(CharacterData, "character_id", character_id, {"image_url": image_url})

    return Response(
        content=f"Image url added to character {character.character_id}",
        status_code=200,
    )


async def load_unmet(user_id: int) -> Response:
    # Load all the character ids
    character_id_list = db.read_all(CharacterData, "character_id")

    # Load all the characters the user has met
    user_character_ids = [
        user_character.character_id
        for user_character in db.read_all(UserCharacter, "user_id", user_id)
    ]

    # Check if there is a character in the list the user has never seen before
    unmet_character_id = None
    for character_id in character_id_list:
        if character_id not in user_character_ids:
            unmet_character_id = character_id
            break
    # If the user has met all the characters in the database:
    if not unmet_character_id:
        return Response(content="No unmet characters for this user", status_code=404)
    # If there's a stored character the user has never seen:
    # Store the relationship in db
    new_user_character = UserCharacter(
        user_id=user_id,
        character_id=unmet_character_id,
    )
    db.store_entry(new_user_character)

    # Load the character full information
    character_data = db.read_from_db(CharacterData, "character_id", unmet_character_id)
    character_profile = db.read_from_db(
        CharacterProfile, "profile_id", character_data.profile_id
    )
    assistant = db.read_from_db(
        CharacterData, "assistant_id", character_data.assistant_id
    )

    return Response(
        content=json.dumps(
            {
                "character": character_profile,
                "assistant": assistant,
                "image_url": character_data.image_url,
            }
        ),
        status_code=200,
    )


# Add character to the database manually
@app.post("/add_character")
async def add_character(request: CharacterCreation, session: SessionDep) -> Response:
    try:
        character_profile = CharacterProfile(
            name=request.name,
            planet_name=request.planet_name,
            personality_traits=request.personality_traits,
            speech_style=request.speech_style,
            quirks=request.quirks,
        )
        db.store_entry(character_profile)
        print(f"Character profile for {request.name} stored successfully.")

        gen_assistant = create_assistant(settings.openai_api_key, request)

        assistant = Assistant(
            assistant_id=gen_assistant.id,
            created_at=gen_assistant.created_at,
            name=gen_assistant.name,
            model=gen_assistant.model,
            instructions=gen_assistant.instructions,
            temperature=gen_assistant.temperature,
        )
        db.store_entry(assistant)
        print(f"New assistant {assistant.name} stored.")

        character_data = CharacterData(
            image_prompt=request.image_prompt,
            image_url=request.image_url,
            assistant_id=assistant.assistant_id,
            profile_id=character_profile.profile_id,
        )
        db.store_entry(character_data)
        print(
            f"{character_profile.name}'s data stored in index {character_data.character_id}"
        )

        return Response(content="New character added successfully.", status_code=201)
    except Exception as e:
        return Response(content=f"Unable to store character: {e}", status_code=500)


# Delete character from the database
@app.delete("/delete_character/{profile_id}")
async def delete_character(character_id: int) -> Response:

    success = delete_character(character_id)

    if success:
        return Response(content=f"Character deleted", status_code=200)

    return Response(status_code=404, content=f"Character not in database")


# @app.post("/character_test")
# async def test_character_creator():
#     response = character_creator(settings.openai_api_key)
#     print(type(response))
#     print(response)
