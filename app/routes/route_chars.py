from fastapi import APIRouter, BackgroundTasks, Response, Depends
from app.config import AppSettings
from app.db.db import DB

from app.services.characters import *

router = APIRouter()


@router.post("/create-character")
async def create_character(
    config: AppSettings = Depends(),
    db: DB = Depends(get_db),
    background_tasks: BackgroundTasks = None,
) -> Response:
    try:
        with db.get_session() as session:

            # 1. Generate new character
            new_character = await generate_character(config.openai_api_key)

            # 2. Generate and store character profile
            generate_profile(config.openai_api_key, db, new_character)

            # 3. Generate and store assistant
            assistant = await generate_assistant(
                config.openai_api_key, db, new_character
            )

            # 4. Generate and store character data
            character_data = generate_character_data(
                config.openai_api_key, db, new_character, assistant
            )

            # 5. Commit the transaction (if everything succeeds)
            session.commit()
            logging.info(
                f"New character created: {character_data.character_profile.name} with ID {character_data.character_id}"
            )

    except Exception as e:
        logging.error(f"Character creation failed: {e}")
        return Response(content=str(e), status_code=500)
    # 6. Generate character portrait in the background
    background_tasks.add_task(
        generate_portrait, config.leonardo_api_key, db, new_character.image_prompt
    )

    return Response(
        content=f"{character_data.character_profile.name} created with ID {character_data.character_id}",
        status_code=201,
    )


# @router.get("/load_character")
# async def load_character_endpoint(background_tasks: BackgroundTasks):
#     return await DB.get_unmet_character()
