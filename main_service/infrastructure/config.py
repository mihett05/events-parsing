from functools import lru_cache

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    cors_origins: list[str] = ["http://localhost:5173"]

    server_host: str = "localhost"
    server_port: int = 8081

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    rabbitmq_host: str
    rabbitmq_port: str
    rabbitmq_user: str
    rabbitmq_password: str

    imap_server: str
    imap_username: str
    imap_password: str

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

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
