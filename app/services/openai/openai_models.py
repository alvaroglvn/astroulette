from pydantic import BaseModel, ValidationError, ConfigDict

from typing import Any, Optional, List


class CharacterProfile(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str


class CharacterData(BaseModel):
    model_config = ConfigDict(strict=True)

    image_prompt: str
    character_profile: CharacterProfile


class Tools(BaseModel):
    type: str


class Assistant(BaseModel):
    model_config = ConfigDict(strict=True)

    id: str
    object: str
    created_at: int
    name: Optional[str]
    description: Optional[str]
    model: str
    instructions: Optional[str]
    tools: Optional[List[Tools]]
    metadata: Optional[List[str]]
    temperature: Optional[float]
    top_p: Optional[float]
    response_format: str = "auto"


def openai_resp_validator(model: BaseModel, response: Any) -> dict[str, Any]:
    try:
        validated_response = model.model_validate_json(response)
    except ValidationError as e:
        print(f"Error parsing data: {e}")

    return validated_response.model_dump()
