import pytest
from application.auth.dtos import AuthenticateUserDto
from application.auth.usecases import LoginUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_login_success(
    get_user_entity: User,
    get_user_authenticate_dto: AuthenticateUserDto,
    login_usecase: LoginUseCase,
):
    test_user, _ = await login_usecase(get_user_authenticate_dto)
    attrs = ("fullname", "email", "id")
    for attr in attrs:
        assert getattr(test_user, attr) == getattr(get_user_entity, attr)
