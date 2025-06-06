from openai import OpenAI
import httpx
import logging
import asyncio

from backend.config.settings import get_settings
from backend.services.leonardo.leon_models import (
    PhoenixPayload,
    ImageGenResponse,
    GenerationInfo,
)


class OpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def build_client(self, project: str | None = None) -> OpenAI:
        """
        Initializes and returns an OpenAI client with the provided API key and optional project name.

        Args:
            project (str | None): Optional project name for the OpenAI client.

        Returns:
            OpenAI: An instance of the OpenAI client.
        """
        return OpenAI(api_key=self.api_key, project=project)


openAI_client = OpenAIClient(api_key=get_settings().openai_api_key).build_client(
    project="proj_iHucBz89WXK9PvH3Hqvf5mhf"
)

# LEONARDO API #


class LeonardoClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.url = "https://cloud.leonardo.ai/api/rest/v1/generations/"

    def get_payload(
        self,
        prompt: str,
        modelId: str = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3",  # Phoenix 1.0
        width: int = 800,
        height: int = 800,
        num_images: int = 1,
        alchemy: bool = False,
        contrast: float = 3.5,
        enhancePrompt: bool = False,
        styleUUID: str | None = "8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd",
        ultra: bool = False,
    ) -> PhoenixPayload:
        return PhoenixPayload(
            modelId=modelId,
            prompt=prompt,
            width=width,
            height=height,
            num_images=num_images,
            alchemy=alchemy,
            contrast=contrast,
            enhancePrompt=enhancePrompt,
            styleUUID=styleUUID,
            ultra=ultra,
        )

    def get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def async_generate_image(self, prompt: str) -> ImageGenResponse:
        url = self.url
        payload = self.get_payload(prompt)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload.model_dump(),
                headers=self.get_headers(),
            )

            assert isinstance(response, httpx.Response)

            if response.status_code == 200:
                return ImageGenResponse(**response.json())
            else:
                raise Exception(f"Failed to generate image: {response.text}")

    async def get_gen_id(self, image_data: ImageGenResponse) -> str:
        return image_data.sdGenerationJob.generationId

    async def get_img_info(self, generation_id: str) -> GenerationInfo:
        url = f"{self.url}{generation_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.get_headers())

            if response.status_code == 200:
                return GenerationInfo(**response.json())
            else:
                raise Exception(f"Failed to retrieve image info: {response.text}")

    async def get_img_status(self, generation_id: str) -> str:
        image_info = await self.get_img_info(generation_id)
        return image_info.generations_by_pk.status

    async def get_img_url(
        self, generation_id: str, max_retries: int, delay: float
    ) -> str | None:
        for _ in range(max_retries):
            status = await self.get_img_status(generation_id)

            if status == "PENDING":
                logging.info("Gathering new image's URL, please wait...")
                await asyncio.sleep(delay)
            elif status == "COMPLETE":
                image_info = await self.get_img_info(generation_id)
                image_url = image_info.generations_by_pk.generated_images[0].url
                logging.info(f"New image ready at {image_url}")
                return image_url
            elif status == "FAILED":
                logging.error("Image generation failed.")
                return None
        logging.error(f"Unable to retrieve new image's URL after {max_retries} retries")
        return None
