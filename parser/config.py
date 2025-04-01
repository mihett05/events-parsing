from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    openai_url: str = "https://openrouter.ai/api/v1"
    openai_model: str = "deepseek/deepseek-chat-v3-0324:free"
    openai_api_key: str


@lru_cache
def get_config() -> Config:
    return Config()
