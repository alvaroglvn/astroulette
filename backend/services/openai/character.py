import random
import logging
import asyncio
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAIError, OpenAI
from backend.schemas import NewCharacter
from backend.config.clients import openai_client


def generate_character(
    client: OpenAI = openai_client.get_client(),
) -> Optional[NewCharacter]:
    """
    Generate a new character via OpenAI and return the character's data and profile.

    Args:
        openai_key (str): OpenAI API key for authentication

    Returns:
        Optional[NewCharacter]: Generated character data and profile as a NewCharacter object.

    Raises:
        OpenAIError: If there is an error with the OpenAI API request.
        Exception: For any other unexpected errors.
    """

    try:
        # Select random values for the prompt
        gender, species, archetype = character_randomizer()

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
                    1. A descriptive **image prompt** tuned for AI-generated art.
                    2. **Character details** useful for interactive dialogue.
                    
                    Follow these instructions to create the data inside the fields:

                    "image_prompt": "Retrofuturism frontal close-up of a {gender} {species} {archetype}, looking straight into the camera. This alien has [describe physical features such as eyes, skin, facial shape, and unique details]. It has a [describe facial expression based on the character's personality]. It wears [describe outfit] inspired by [insert a fashion designer]. Background is a colorful mod pattern.",

                    
                    "name": "[Generate a unique name for this alien]",
                    "planet_name": [Unique name for this alien's homeplanet]
                    "planet_description": [Main characteristics of the home planet and how its nature impacts its inhabitants] 
                    "personality_traits": "[Personality traits that would come apparent as the alien speaks.]",
                    "speech_style": "[Explain how they express themselves (e.g. are they cryptic? humorous? regal? cold? poetic? etc.)]",
                    "quirks": "[Any quirky speech habits, or unique expressions they tend to use.]"
                    "human_relationship": [How they see humans (eg. Are they curious? Friendly? Hostile? Pleasant? Distrustful? Uninterested? etc. This should impact their conversation.)]
                    """,
                },
            ],
            response_format=NewCharacter,
        )

        return response.choices[0].message.parsed

    except OpenAIError as e:
        logging.error(f"Error generating character with OpenAI: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def character_randomizer() -> tuple[str, str, str]:
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

    return random.choice(gender), random.choice(species), random.choice(archetypes)


# Concurrency for generating characters
executor = ThreadPoolExecutor()


async def generate_character_async(
    client: OpenAI = openai_client.get_client(),
) -> Optional[NewCharacter]:
    """
    This function is a wrapper for the generate_character function to run it in a separate thread.
    It uses asyncio's run_in_executor to allow for non-blocking behavior in an async context.
    Args:
        openai_key (str): OpenAI API key for authentication
    Returns:
        Optional[NewCharacter]: Generated character data and profile as a NewCharacter object.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, generate_character, client)
