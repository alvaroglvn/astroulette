from typing import Type, TypeVar, Optional
from pydantic import ValidationError
import logging


T = TypeVar("T", bound=Type)


def validate_data(model: Type[T], response: str) -> Optional[T]:
    """
    Validates any data using a given Pydantic model and returns the model instance.

    Args:
        model (Type[T]): The Pydantic model class to validate the response against.
        response (str): The JSON response string to be validated.

    Returns:
        Optional[T]: An instance of the Pydantic model if validation is successful, otherwise None.

    Raises:
        ValidationError: If the response cannot be validated against the model.
    """

    try:
        return model.model_validate_json(response)
    except ValidationError as e:
        logging.error(f"Validation failed: {e}")
        return None
