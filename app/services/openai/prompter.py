from openai import OpenAI


def character_prompter(openai_key: str) -> str:
    client = OpenAI(api_key=openai_key, project="proj_iHucBz89WXK9PvH3Hqvf5mhf")
    new_character = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": "You are an accurate and efficient AI prompter for generative art for science fiction characters. You're an expert in creating uncanny an unique characters.",
            },
            {
                "role": "user",
                "content": """Return this prompt filling the gaps: 1950s science fiction meets cyberpunk, frontal medium shot of [one word personality trait] [pick one at random: male, female] [pick one at random: humanoid, robot, animal, or monster] alien looking straight into the camera. [Longer description of the character optimized for image generation] The clothes are inspired by [name a fashion designer]. The background is related to the alien's [element] planet, which also makes the color palette.
                """,
            },
        ],
    )
    print(new_character.model_dump())
    return new_character.choices[0].message.content
