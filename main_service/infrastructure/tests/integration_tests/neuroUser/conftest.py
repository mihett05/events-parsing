from datetime import datetime
from typing import Callable

import pytest

from infrastructure.api.v1.users.dtos import UpdateUserModelDto
from infrastructure.api.v1.users.models import UserModel


@pytest.fixture
def user_model_factory() -> Callable[[...], UserModel]:
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
def update_user_model_dto_factory() -> Callable[[...], UpdateUserModelDto]:
    def _factory(
        fullname: str = "Updated Name", telegram_id: int | None = 123456789
    ) -> UpdateUserModelDto:
        return UpdateUserModelDto(fullname=fullname, telegramId=telegram_id)

    return _factory
