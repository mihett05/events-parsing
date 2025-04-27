import pytest_asyncio

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto, CreateUserModelDto


@pytest_asyncio.fixture
async def get_authenticate_user_model_dto() -> AuthenticateUserModelDto:
    return AuthenticateUserModelDto(
        email="test@test.com",
        password="12345678"
    )

@pytest_asyncio.fixture
async def get_create_user_model_dto() -> CreateUserModelDto:
    return CreateUserModelDto(
        email="test@test.com",
        password="12345678",
        fullname="Ivanov Ivan Ivanovich",
        isActive=True
    )