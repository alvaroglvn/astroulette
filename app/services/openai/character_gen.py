from openai import OpenAI
import random

from app.db.db_models import *

from app.services.openai.openai_models import CharacterData, openai_resp_validator


def character_generator(openai_key: str) -> CharacterData | None:
    """This function creates a fantasy character using OpenAI's GPT-4 model. It returns a JSON object with an image prompt and a character profile that can later be pipelined into other APIs for generating art or dialogue."""

    # Select random values for the prompt
    archetypes = [
        "elder alien",
        "cosmic sage",
        "dark overlord",
        "bio-mechanical alien",
        "trickster alien",
        "impish being",
        "diplomatic alien",
        "alien rockstar",
        "alien celebrity",
        "silent observer",
        "space pirate",
        "galactic emperor",
        "galactic royal",
        "alien supermodel",
        "space vampire",
        "alien zombie",
        "alien supersoldier",
        "mad scientist",
        "galactic divine being",
        "galactic demon",
    ]
    gender = ["male", "female"]
    species = [
        "humanoid",
        "robot",
        "insectoid",
        "beast",
        "amphibian",
        "reptilian",
        "animalistic",
        "monster",
        "cyborg",
        "mutant",
        "mineral based",
        "plant based",
        "rock based",
    ]

    # Make chat request to OpenAI
    client = OpenAI(api_key=openai_key, project="proj_iHucBz89WXK9PvH3Hqvf5mhf")
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": "You are a character designer with expertise in unique and exciting retro futurism characters.",
            },
            {
                "role": "user",
                "content": f"""
                Generate a unique alien character with both:
                1. A detailed **image prompt** for AI-generated art.
                2. A **personality & behavior profile** for interactive dialogue.
                
                Follow this instructions to create the data inside the fields:

                "image_prompt": "Vibrant colors frontal close-up of a {random.choice(gender)} {random.choice(species)} {random.choice(archetypes)}, looking straight into the camera. This alien has [describe physical features such as eyes, skin, shape, unique details]. It has a [describe facial expression based on personality]. It wears [describe outfit] inspired by [insert a fashion designer]. Background is a colorful mod pattern.",

                "character_profile": 
                    "name": "[Generate a unique name for this alien]",
                    "planet_name": [Unique name for this alien's homeplanet]
                    "planet_description": [Main characteristics of the homeplanet and how its nature impacts its inhabitants] 
                    "personality_traits": "[Describe facial expression based on personality]",
                    "speech_style": "[Describe how they talk (e.g., cryptic, humorous, regal, cold, poetic)]",
                    "quirks": "[Any strange speech habits, or expressions that make them unique.]"
                """,
            },
        ],
        response_format=CharacterData,
    )

    # Select new character information
    new_character = response.choices[0].message.content

    validate_character = openai_resp_validator(CharacterData, new_character)
    print(validate_character)
    return validate_character
