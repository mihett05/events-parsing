import random
import shutil
import string
from typing import Callable

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
async def setup_db_tables(
        pytestconfig: pytest.Config, container: AsyncContainer
):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_data(pytestconfig: pytest.Config, container: AsyncContainer):
    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
            )


@pytest_asyncio.fixture(scope="session")
async def get_app(container: AsyncContainer):
    app = create_app(container, await container.get(Config))
    yield app
    shutil.rmtree("static")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_client(get_app: FastAPI) -> AsyncClient:
    transport = ASGITransport(app=get_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


# -------------------------------------------------------
# -------------------- FACTORIES ------------------------
# -------------------------------------------------------


@pytest.fixture
def create_user_model_dto_factory() -> Callable[..., CreateUserModelDto]:
    def _factory(
            email: str = "test@example.com",
            password: str = "12345678",
            fullname: str = "Test User",
            is_active: bool = True,
    ) -> CreateUserModelDto:
        return CreateUserModelDto(
            email=email,
            password=password,
            fullname=fullname,
            isActive=is_active,
        )

    return _factory


@pytest.fixture
def authenticate_dto_factory() -> Callable[..., AuthenticateUserModelDto]:
    def _factory(
            email: str = "test@example.com",
            password: str = "12345678",
    ) -> AuthenticateUserModelDto:
        return AuthenticateUserModelDto(email=email, password=password)

    return _factory


@pytest_asyncio.fixture(autouse=True)
async def create_user(create_user_model_dto_factory, async_client) -> UserWithTokenModel:
    response = await async_client.post(
        "/v1/auth/register",
        json=create_user_model_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    model = UserWithTokenModel(**response.json())
    yield model
    await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {model.access_token}"},
    )


@pytest_asyncio.fixture
async def user_with_token_model(
        create_user, authenticate_dto_factory, async_client
) -> UserWithTokenModel:
    response = await async_client.post(
        "/v1/auth/login",
        json=authenticate_dto_factory().model_dump(by_alias=True, mode="json"),
    )
    model = UserWithTokenModel(**response.json())
    yield model
    await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {model.access_token}"},
    )


@pytest.fixture
def random_string_factory() -> Callable[..., str]:
    def random_string(lenght: int) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=lenght))

    return random_string


@pytest.fixture
def random_email_factory(random_string_factory) -> Callable[..., str]:
    def random_email() -> str:
        return f"{random_string_factory(10)}@{random_string_factory(5)}.com"

    return random_email
