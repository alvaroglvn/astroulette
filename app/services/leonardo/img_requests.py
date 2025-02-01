import httpx
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class LeonardoSettings(BaseSettings):
    api_key: str

    class Config:
        env_file = ".env"


settings = LeonardoSettings()


headers = {
    "Authorization": f"Bearer {settings.api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

urls = {"generate": "https://api.leonardocloud.com/v1/vision/general"}


class PhoenixPayload(BaseModel):
    modelId: str = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"  # Phoenix 1.0
    prompt: str
    width: Optional[int] = 800
    height: Optional[int] = 800
    num_images: Optional[int] = 1
    alchemy: Optional[bool] = False  # False for Fast, True for High Quality
    contrast: Optional[float] = 3.5  # Low=3, Medium=3.5, High=4
    enhancePrompt: Optional[bool] = False  # True=ON, False=OFF
    styleUUID: Optional[str] = "556c1ee5-ec38-42e8-955a-1e82dad0ffa1"
    ultra: Optional[bool] = False


async def generate_image(apikey: str = settings.api_key) -> None:
    payload = PhoenixPayload(
        prompt="A beautiful sunset over the city",
        width=800,
        height=800,
        styleUUID="556c1ee5-ec38-42e8-955a-1e82dad0ffa1",
    )

    async with httpx.AsyncClient() as client:
        r = await client.post(
            urls["generate"], json=payload.model_dump(), headers=headers
        )
        print(r.status_code)
