import pytest

from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import RegisterUseCase
from application.users.usecases import CreateUserUseCase


@pytest.mark.asyncio
async def test_create_success(
    create_user_usecase: CreateUserUseCase,
    register_user_usecase: RegisterUseCase,
    register_user_dto: RegisterUserDTO,
):
    user, _ = await register_user_usecase(dto=register_user_dto)

    attrs = ("fullname", "email")
    for attr in attrs:
        assert getattr(user, attr) == getattr(register_user_dto, attr)

    assert user.id == 1
