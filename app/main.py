from typing import Annotated, AsyncGenerator, Generator

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from sqlmodel import Session

from app.db.db import DB
from app.db.db_models import *

from app.config import AppSettings
from app.models import *


# Load app settings
settings = AppSettings()

# Load database
db = DB("app/db/alien_talk.sqlite")


# Load DB dependency
def get_db() -> DB:
    return db


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


# MAIN API FUNCTIONALITY
# @app.get(f"/alien-talk/{1}")
# async def start_session(user_id: int, background_tasks: BackgroundTasks) -> Response:
#     """Main app functionality.
#     a) If there's a character in the database the user has never seen, it loads it.
#     b) If there are none,  we generate a new character and add it to the database.
#     We then pass either response to a WebSocket function to build the actual chat."""
#     response = await load_from_db()

#     if response:
#         # Load character from DB to websocket
#         pass

#     # gen_character =


# #     if response.status_code == 404:
# #         response = await generate_character(user_id, background_tasks)

# #     return await load_chat(response)


# # async def load_chat(character_response: Response) -> Response:
# #     """Pipelines the character selection to the chat session"""
# #     if character_response.status_code != 200 or character_response.status_code != 201:
# #         return Response(content="Failed to load character", status_code=500)

# #     character_data = json.loads(character_response.content)

# #     return await load_assistant(character_data["assistant"])


# @app.get("/load_character")
# async def load_from_db() -> CharacterResponse | None:
#     # Check for characters in database user has not met.
#     character_from_db = db.get_unmet_character(1)

#     if character_from_db:
#         character_id = character_from_db.character_id
#         new_user_character = UserCharacter(user_id=1, character_id=character_id)
#         # Store relationship user/character
#         db.store_entry(new_user_character)

#         # Load character info and build JSON response
#         character_profile = db.read_from_db(
#             CharacterProfile, "profile_id", character_from_db.profile_id
#         )
#         assistant = db.read_from_db(
#             Assistant, "assistant_id", character_from_db.assistant_id
#         )

#         return CharacterResponse(
#             character_profile=character_profile,
#             assistant=assistant,
#             image_url=character_from_db.image_url,
#         )
#     return None


# # Generate new character and add it to the database
# @app.post("/generate_character")
# async def generate_character(
#     background_tasks: BackgroundTasks,
# ) -> Response:

#     retries = 0
#     max_retries = 3
#     while retries < max_retries:
#         try:

#             # Generate new character
#             character_gen = character_generator(settings.openai_api_key)

#             if character_gen:
#                 # Build and store character profile
#                 character_profile = CharacterProfile(
#                     name=character_gen.character_profile.name,
#                     planet_name=character_gen.character_profile.planet_name,
#                     planet_description=character_gen.character_profile.planet_description,
#                     personality_traits=character_gen.character_profile.personality_traits,
#                     speech_style=character_gen.character_profile.speech_style,
#                     quirks=character_gen.character_profile.quirks,
#                 )
#                 db.store_entry(character_profile)
#                 print(f"{character_profile.name} stored in db.")

#                 # Build and store character's assistant
#                 assistant_gen = create_assistant(settings.openai_api_key, character_gen)

#                 if assistant_gen:
#                     assistant = Assistant(
#                         assistant_id=assistant_gen.id,
#                         created_at=assistant_gen.created_at,
#                         name=assistant_gen.name,
#                         model=assistant_gen.model,
#                         instructions=assistant_gen.instructions,
#                         temperature=assistant_gen.temperature,
#                     )
#                     db.store_entry(assistant)
#                     print(f"{assistant.name} added to db.")
#                 else:
#                     raise SystemError(
#                         f"Unable to create new assistant for        {character_profile.name}"
#                     )

#                 # Create and store character data
#                 character_data = CharacterData(
#                     image_prompt=character_gen.image_prompt,
#                     assistant_id=assistant.assistant_id,
#                     profile_id=character_profile.profile_id,
#                 )
#                 db.store_entry(character_data)
#                 print(f"Character data for {character_profile.name}  stored in db.")

#                 # Queue image generation in the background
#                 background_tasks.add_task(
#                     character_portrait, character_data.character_id
#                 )

#                 return Response(
#                     content="New character generated successfully!", status_code=201
#                 )
#         except Exception as e:
#             retries += 1
#             print(f"Error {e}. Retrying: {retries} of {max_retries}...")

#     return Response(content="Unable to generate new character", status_code=500)


# async def character_portrait(character_id: int) -> Response:
#     # Load character
#     character = db.read_from_db(CharacterData, "character_id", character_id)

#     # Generate character's portrait
#     payload = PhoenixPayload(
#         prompt=character.image_prompt,
#         width=800,
#         height=800,
#         num_images=1,
#         alchemy=False,
#         contrast=4,
#         enhancePrompt=False,
#         styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84",  #    Vibrant
#         ultra=False,
#     )
#     image_url = await generate_image(settings.leonardo_api_key, payload)

#     # Update character with image url
#     db.update_db(CharacterData, "character_id", character_id, {"image_url": image_url})

#     return Response(
#         content=f"Image url added to character {character.character_id}",
#         status_code=200,
#     )


# Add character to the database manually
# @app.post("/add_character")
# async def add_character(request: CharacterCreation, session: SessionDep) -> Response:
#     try:
#         character_profile = CharacterProfile(
#             name=request.name,
#             planet_name=request.planet_name,
#             personality_traits=request.personality_traits,
#             speech_style=request.speech_style,
#             quirks=request.quirks,
#         )
#         db.store_entry(character_profile)
#         print(f"Character profile for {request.name} stored successfully.")

#         gen_assistant = create_assistant(settings.openai_api_key, request)

#         assistant = Assistant(
#             assistant_id=gen_assistant.id,
#             created_at=gen_assistant.created_at,
#             name=gen_assistant.name,
#             model=gen_assistant.model,
#             instructions=gen_assistant.instructions,
#             temperature=gen_assistant.temperature,
#         )
#         db.store_entry(assistant)
#         print(f"New assistant {assistant.name} stored.")

#         character_data = CharacterData(
#             image_prompt=request.image_prompt,
#             image_url=request.image_url,
#             assistant_id=assistant.assistant_id,
#             profile_id=character_profile.profile_id,
#         )
#         db.store_entry(character_data)
#         print(
#             f"{character_profile.name}'s data stored in index {character_data.character_id}"
#         )

#         return Response(content="New character added successfully.", status_code=201)
#     except Exception as e:
#         return Response(content=f"Unable to store character: {e}", status_code=500)


# # Delete character from the database
# @app.delete("/delete_character/{profile_id}")
# async def delete_character(character_id: int) -> Response:

#     success = delete_character(character_id)

#     if success:
#         return Response(content=f"Character deleted", status_code=200)

#     return Response(status_code=404, content=f"Character not in database")


# @app.post("/character_test")
# async def test_character_creator():
#     response = character_creator(settings.openai_api_key)
#     print(type(response))
#     print(response)
