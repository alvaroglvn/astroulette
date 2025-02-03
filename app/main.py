# from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import openai

from app.config import AppSettings
from app.services.leonardo.img_request import PhoenixPayload, generate_image
from app.services.openai.prompter import character_prompter


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
async def generate() -> dict:
    new_character = character_prompter(settings.openai_api_key)

    payload = PhoenixPayload(
        prompt=new_character,
        width=800,
        height=800,
        num_images=1,
        alchemy=False,
        contrast=4,
        enhancePrompt=False,
        styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd",  # Portrait
        ultra=False,
    )

    response = await generate_image(settings.leonardo_api_key, payload)
    return response.json()
