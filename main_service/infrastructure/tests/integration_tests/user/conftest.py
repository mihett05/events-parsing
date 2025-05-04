from datetime import datetime
from typing import Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from infrastructure.api.v1.auth.dtos import (
    CreateUserModelDto,
)
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.dtos import UpdateUserModelDto
from infrastructure.api.v1.users.models import UserModel


@pytest.fixture
def user_model_factory() -> Callable[[], UserModel]:
    def _factory(
        id: int = 1,
        email: str = "test@example.com",
        fullname: str = "Test User",
        is_active: bool = True,
        telegram_id: int | None = None,
        created_at: datetime = datetime.now(),
    ) -> UserModel:
        return UserModel(
            id=id,
            email=email,
            fullname=fullname,
            isActive=is_active,
            telegramId=telegram_id,
            createdAt=created_at,
        )

    return _factory


@pytest.fixture
def update_user_model_dto_factory(random_string_factory, random_number_factory) -> Callable[[], UpdateUserModelDto]:
    def _factory(
        fullname: str = random_string_factory(10), telegram_id: int | None = random_number_factory(5)
    ) -> UpdateUserModelDto:
        return UpdateUserModelDto(fullname=fullname, telegramId=telegram_id)

    return _factory


@pytest_asyncio.fixture
async def get_create_user_model_dtos() -> list[CreateUserModelDto]:
    return [
        CreateUserModelDto(
            email=f"test{i}@test.com",
            password=f"{i}2345678",
            fullname=f"Ivan{i}",
            isActive=True,
        )
        for i in range(8)
    ]


@pytest_asyncio.fixture
async def create_users(
    async_client: AsyncClient,
    get_create_user_model_dtos: list[CreateUserModelDto],
) -> list[UserWithTokenModel]:
    models = []
    for dto in get_create_user_model_dtos:
        response = await async_client.post(
            "/v1/auth/register",
            json=dto.model_dump(by_alias=True, mode="json")
        )
        models.append(UserWithTokenModel(**response.json()))
    yield models
    for model in models:
        await async_client.delete(
            "/v1/users/",
            headers={"Authorization": f"Bearer {model.access_token}"},
        )
