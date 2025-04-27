from datetime import datetime

import pytest_asyncio

from infrastructure.api.v1.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)
from infrastructure.api.v1.users.models import UserModel


@pytest_asyncio.fixture
async def get_authenticate_user_model_dto() -> AuthenticateUserModelDto:
    return AuthenticateUserModelDto(email="test@test.com", password="12345678")


@pytest_asyncio.fixture
async def get_create_user_model_dto() -> CreateUserModelDto:
    return CreateUserModelDto(
        email="test@test.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
        isActive=True,
    )


@pytest_asyncio.fixture
async def get_user_model() -> UserModel:
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
