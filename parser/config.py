from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    openai_url: str = "https://openrouter.ai/api/v1"
    openai_model: str = "deepseek/deepseek-chat-v3-0324:free"
    openai_api_key: str

    rabbitmq_host: str
    rabbitmq_port: str
    rabbitmq_user: str
    rabbitmq_password: str

    @computed_field
    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@"
            f"{self.rabbitmq_host}:{self.rabbitmq_port}/"
        )


@lru_cache
def get_config() -> Config:
    return Config()
