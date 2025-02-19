from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env")

    leonardo_api_key: str
    openai_api_key: str
    login_key: str


class EmailConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="app/.env")

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_SSL_TLS: bool
