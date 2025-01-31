from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    leonardo_api_key: str
    openai_api_key: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
