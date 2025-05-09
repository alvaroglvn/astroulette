from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class AppSettings(BaseSettings):

    secret_key: str

    leonardo_api_key: str
    openai_api_key: str
    login_key: str

    db_url: str

    mailgun_domain: str
    mailgun_api_key: str
    from_email: str

    cookie_domain: str
    frontend_url: str

    model_config = SettingsConfigDict(env_file="app/.env", extra="ignore")


@lru_cache
def get_settings() -> AppSettings:
    """
    Provides an instance of the AppSettings class.

    This function serves as a dependency provider for the application settings, ensuring that an instance of AppSettings is available wherever it is needed.

    Returns:
        AppSettings: An instance of the AppSettings class.
    """
    return AppSettings()  # type: ignore[call-arg]


settings_dependency = Annotated[AppSettings, Depends(get_settings)]
