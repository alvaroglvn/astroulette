# from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import AppSettings
from app.services.leonardo.img_request import PhoenixPayload, generate_image
from app.services.openai.prompter import character_creator


settings = AppSettings()

app = FastAPI()

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
async def generate(max_retries: int = 3) -> None:
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
                styleUUID="dee282d3-891f-4f73-ba02-7f8131e5541b",  # Vibrant
                ultra=False,
            )

            await generate_image(settings.leonardo_api_key, payload)
            print("Character generation succesful!")
            return

        retries += 1
        print(f"Retry {retries} of {max_retries}...")

    print("Character generation failed")
    return None
