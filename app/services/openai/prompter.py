from openai import OpenAI
import random
from pydantic import BaseModel, ConfigDict, ValidationError
import json


def character_creator(openai_key: str) -> dict | None:
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
    ]

    # Make chat request to OpenAI
    client = OpenAI(api_key=openai_key, project="proj_iHucBz89WXK9PvH3Hqvf5mhf")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": "You are a character designer with expertise in unique and exciting retro scifi characters.",
            },
            {
                "role": "user",
                "content": f"""
                Generate a unique alien character with both:
                1. A detailed **image prompt** for AI-generated art.
                2. A **personality & behavior profile** for interactive dialogue.
                
                Return the result **strictly** as a valid JSON object with two fields: `image_prompt` and `character_profile`.

                ```json
                {{
                    "image_prompt": "Frontal close-up of a {random.choice(gender)} {random.choice(species)} {random.choice(archetypes)}, looking straight into the camera. This alien has [describe physical features such as eyes, skin, shape, unique details]. It has a [describe facial expression based on personality]. It wears [describe outfit] inspired by [insert a fashion designer]. Background is a colorful mod pattern.",

                    "character_profile": {{
                        "name": "[Generate a unique name for this alien]",
                        "personality_traits": "[escribe facial expression based on personality]",
                        "speech_style": "[Describe how they talk (e.g., cryptic, humorous, regal, cold, poetic)]",
                        "quirks": "[Any strange habits, or expressions that make them unique.]"
                    }}```
                }}
                """,
            },
        ],
    )
    raw_data = response.choices[0].message.content.strip()

    # Character data validation
    validated_data = character_validator(raw_data)

    return validated_data


def character_validator(raw_data: str) -> dict:
    """This function validates the JSON object returned by OpenAI's GPT-4 model for generating a fantasy character. It checks if the object has the required fields and values, and returns the parsed data if valid."""

    class CharacterProfile(BaseModel):
        model_config = ConfigDict(strict=True)

        name: str
        personality_traits: str
        speech_style: str
        quirks: str

    class CharacterResponse(BaseModel):
        model_config = ConfigDict(strict=True)

        image_prompt: str
        character_profile: CharacterProfile

    # Strip markdown formatting
    if raw_data.startswith("```json"):
        raw_data = raw_data[7:]  # Remove the leading ```json
    if raw_data.endswith("```"):
        raw_data = raw_data[:-3]  # Remove the trailing ```

    try:
        validated_data = CharacterResponse.model_validate_json(raw_data)
    except ValidationError as e:
        print(f"Error parsing JSON: {e}")
        return None

    return validated_data.model_dump()
