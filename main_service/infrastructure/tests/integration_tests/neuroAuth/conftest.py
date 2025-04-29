from typing import Callable, Optional

import pytest

from infrastructure.api.v1.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.fixture
def create_user_model_dto_factory() -> Callable[[...], CreateUserModelDto]:
    def _factory(
        email: str = "test@example.com",
        password: str = "password123",
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
def authenticate_user_model_dto_factory() -> Callable[
    [...], AuthenticateUserModelDto
]:
    def _factory(
        email: str = "test@example.com", password: str = "password123"
    ) -> AuthenticateUserModelDto:
        return AuthenticateUserModelDto(email=email, password=password)

    return _factory


@pytest.fixture
def user_with_token_model_factory(
    user_model_factory,
) -> Callable[[...], UserWithTokenModel]:
    def _factory(
        access_token: str = "fake-jwt-token", user: Optional[UserModel] = None
    ) -> UserWithTokenModel:
        return UserWithTokenModel(
            accessToken=access_token, user=user or user_model_factory()
        )

    return _factory
