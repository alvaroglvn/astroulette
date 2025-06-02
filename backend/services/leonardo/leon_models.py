from typing import Optional, List
from pydantic import BaseModel


# Image gen payload for request
class PhoenixPayload(BaseModel):
    modelId: str = "de7d3faf-762f-48e0-b3b7-9d0ac3a3fcf3"  # Phoenix 1.0
    prompt: str
    width: Optional[int] = 800
    height: Optional[int] = 800
    num_images: Optional[int] = 1
    alchemy: Optional[bool] = False  # False for Fast, True for High Quality
    contrast: Optional[float] = 3.5  # Low=3, Medium=3.5, High=4
    enhancePrompt: Optional[bool] = False  # True=ON, False=OFF
    styleUUID: Optional[str] = "8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd"
    ultra: Optional[bool] = False


# Image generation response
class sdGenerationJob(BaseModel):
    generationId: str
    apiCreditCost: int


class ImageGenResponse(BaseModel):
    sdGenerationJob: sdGenerationJob


# Single generation info response
class GeneratedImage(BaseModel):
    url: str


class GenerationByPk(BaseModel):
    status: str
    generated_images: List[GeneratedImage]


class GenerationInfo(BaseModel):
    generations_by_pk: GenerationByPk
