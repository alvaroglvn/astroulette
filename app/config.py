from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env")

    leonardo_api_key: str
    openai_api_key: str
