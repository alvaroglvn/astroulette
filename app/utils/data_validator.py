from pydantic import ValidationError, BaseModel
from typing import Type, TypeVar
import logging


T = TypeVar("T", bound=BaseModel)


def validate_data(model: Type[T], response: str) -> T | None:
    """Validates any data using a given Pydantic model and returns the model instance"""
    try:
        return model.model_validate_json(response)
    except ValidationError as e:
        logging.error(f"Validation failed: {e}")
        return None
