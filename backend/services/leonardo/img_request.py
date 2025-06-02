import httpx
import asyncio
from backend.services.leonardo.leon_models import (
    PhoenixPayload,
    ImageGenResponse,
    GenerationInfo,
)


urls = {
    "generate": "https://cloud.leonardo.ai/api/rest/v1/generations",
    "get_info": "https://cloud.leonardo.ai/api/rest/v1/generations/",
}

# TODO: Similar to my note in `openai`, rather than passing in the API key as a parameter, you can pass in a client. But in this case, the client can just be a fetchLeo(method, url, body) function that returns response_info.
async def generate_portrait(apikey: str, prompt: str) -> str | None:
    payload = PhoenixPayload(prompt=prompt)

    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Step 1: Generate new image
    async with httpx.AsyncClient() as client:
        response_gen = await client.post(
            urls["generate"], json=payload.model_dump(), headers=headers
        )
        if response_gen.status_code == 200:
            response_gen_data = ImageGenResponse(**response_gen.json())
            generation_id = response_gen_data.sdGenerationJob.generationId

            # After we know the image is being generated, we need to retrieve its information
            max_retries = 10
            delay = 1

            for _ in range(max_retries):
                async with httpx.AsyncClient() as client:
                    response_info = await client.get(
                        f"{urls["get_info"]}{generation_id}", headers=headers
                    )
                    response_info_data = GenerationInfo(**response_info.json())
                    status = response_info_data.generations_by_pk.status

                    print(f"Current status is {status}")

                    if status == "PENDING":
                        print("Gathering new image's url, please wait...")
                    elif status == "COMPLETE":
                        image_url = (
                            response_info_data.generations_by_pk.generated_images[0].url
                        )
                        print(f"New image ready at {image_url}")
                        return image_url
                    elif status == "FAILED":
                        print("Image generation failed.")
                        return None
                    await asyncio.sleep(delay)

            print(f"Unable to retrieve new image's url after {max_retries} retries")
            return None
        return None
