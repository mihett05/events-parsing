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
    return AuthenticateUserModelDto(email="test@example.com", password="12345678")


@pytest_asyncio.fixture
async def get_create_user1_model_dto() -> CreateUserModelDto:
    return CreateUserModelDto(
        email="test@example.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
        isActive=True,
    )


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
async def get_user1_model() -> UserModel:
    return UserModel(
        **{
            "id": 1321,
            "email": "test@example.com",
            "fullname": "Ivanov Ivan Ivanovich",
            "isActive": True,
            "telegramId": None,
            "created_at": datetime.now(),
        }
    )


@pytest_asyncio.fixture
async def create_user1(
        async_client: AsyncClient, get_create_user1_model_dto: CreateUserModelDto
):
    response = await async_client.post(
        "/v1/auth/register",
        json=get_create_user1_model_dto.model_dump(by_alias=True, mode="json"),
    )
    response_model = UserWithTokenModel(**response.json())
    yield response_model

    await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {response_model.access_token}"},
    )


@pytest_asyncio.fixture
async def create_users(
        async_client: AsyncClient,
        get_create_user_model_dtos: list[CreateUserModelDto],
):
    responses = []
    for dto in get_create_user_model_dtos:
        responses.append(
            await async_client.post(
                "/v1/auth/register",
                json=dto.model_dump(by_alias=True, mode="json"),
            )
        )
    yield None
    for response in responses:
        response_model = UserWithTokenModel(**response.json())
        await async_client.delete(
            "/v1/users/",
            headers={"Authorization": f"Bearer {response_model.access_token}"},
        )
