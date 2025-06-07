import logging
from backend.config.clients import LeonardoClient


async def generate_portrait(client: LeonardoClient, prompt: str) -> str | None:

    try:
        image_gen = await client.async_generate_image(prompt=prompt)
        gen_id = await client.get_gen_id(image_gen)
        image_url = await client.get_img_url(gen_id, 10, 1.0)

        assert isinstance(image_url, str), "Image URL should be a string"
        return image_url
    except Exception as e:
        logging.error(f"Error generating portrait: {e}")
        return None
