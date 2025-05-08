from functools import lru_cache
from pathlib import Path

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

    secret_key: str
    imap_server: str
    imap_username: str
    imap_password: str

    telegram_bot_token: str

    minio_root_host: str
    minio_root_port: str
    minio_root_user: str
    minio_root_password: str
    minio_bucket_name: str = "attachments"
    smtp_server: str
    smtp_port: int
    static_folder: Path = Path("static/")

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

    @computed_field
    @property
    def minio_url(self) -> str:
        return f"{self.minio_root_host}:{self.minio_root_port}"


@lru_cache
def get_config() -> Config:
    return Config()


@lru_cache
def get_mock_config() -> Config:
    return Config(_env_file=".dev.env", _env_file_encoding="utf-8")
