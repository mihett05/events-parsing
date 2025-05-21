import random
import shutil
import string
from typing import Any, Callable, Coroutine

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.api.app import create_app
from infrastructure.api.v1.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.config import Config
from infrastructure.database.postgres import Base
from infrastructure.tests.configs import get_container


@pytest_asyncio.fixture(scope="session")
async def container(pytestconfig: pytest.Config):
    async with get_container(True) as container:
        try:
            yield container
        finally:
            await container.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_tables(pytestconfig: pytest.Config, container: AsyncContainer):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_data(pytestconfig: pytest.Config, container: AsyncContainer):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE"))


@pytest_asyncio.fixture(scope="session")
async def get_app(container: AsyncContainer):
    app = create_app(container, await container.get(Config))
    yield app
    shutil.rmtree("static")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_client(get_app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=get_app)
    async with AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client


# -------------------------------------------------------
# -------------------- FACTORIES ------------------------
# -------------------------------------------------------


@pytest.fixture(scope="function")
def create_user_model_dto_factory(
    random_string_factory, random_email_factory
) -> Callable[..., CreateUserModelDto]:
    def _factory(
        email: str | None = None,
        password: str = "12345678",
        fullname: str | None = None,
        is_active: bool = True,
    ) -> CreateUserModelDto:
        return CreateUserModelDto(
            email=email or f"{random_email_factory()}",
            password=password,
            fullname=fullname or f"{random_string_factory(10)}",
            isActive=is_active,
        )

    return _factory


@pytest.fixture(scope="function")
def authenticate_dto_factory() -> Callable[..., AuthenticateUserModelDto]:
    def _factory(
        email: str = "test@example.com",
        password: str = "12345678",
    ) -> AuthenticateUserModelDto:
        return AuthenticateUserModelDto(email=email, password=password)

    return _factory


@pytest_asyncio.fixture(scope="function", autouse=True)
async def user_with_token_model(
    create_user_model_dto_factory, async_client
) -> Callable[[], Coroutine[Any, Any, UserWithTokenModel]]:
    async def _factory():
        response = await async_client.post(
            "/v1/auth/register",
            json=create_user_model_dto_factory().model_dump(by_alias=True, mode="json"),
        )
        return UserWithTokenModel(**response.json())

    return _factory


@pytest.fixture(scope="function")
def random_string_factory() -> Callable[..., str]:
    def random_string(lenght: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=lenght))

    return random_string


@pytest.fixture(scope="function")
def random_email_factory(random_string_factory) -> Callable[..., str]:
    def random_email() -> str:
        return f"{random_string_factory(10)}@{random_string_factory(5)}.com"

    return random_email


@pytest.fixture
def random_number_factory() -> Callable[..., int]:
    def random_number(lenght: int) -> int:
        return int("".join(random.choices(string.digits, k=lenght)))

    return random_number
