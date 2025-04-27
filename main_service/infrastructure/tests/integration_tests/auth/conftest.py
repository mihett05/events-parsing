from datetime import datetime

import pytest_asyncio
from httpx import AsyncClient

from infrastructure.api.v1.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest_asyncio.fixture
async def get_authenticate_user1_model_dto() -> AuthenticateUserModelDto:
    return AuthenticateUserModelDto(email="test@test.com", password="12345678")


@pytest_asyncio.fixture
async def get_create_user1_model_dto() -> CreateUserModelDto:
    return CreateUserModelDto(
        email="test@test.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
        isActive=True,
    )


@pytest_asyncio.fixture
async def get_user1_model() -> UserModel:
    return UserModel(
        **{
            "id": 1321,
            "email": "test@test.com",
            "fullname": "Ivanov Ivan Ivanovich",
            "isActive": True,
            "telegramId": None,
            "created_at": datetime.now(),
        }
    )

@pytest_asyncio.fixture
async def create_user1(
    get_test_client: AsyncClient,
    get_create_user1_model_dto: CreateUserModelDto
):
    response = await get_test_client.post(
        "/v1/auth/register",
        json=get_create_user1_model_dto.model_dump(by_alias=True, mode="json"),
    )
    yield None
    response_model = UserWithTokenModel(**response.json())
    await get_test_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {response_model.access_token}"}
    )