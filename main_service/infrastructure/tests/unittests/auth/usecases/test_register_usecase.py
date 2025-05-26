import pytest
from application.auth.dtos import RegisterUserDto
from application.auth.usecases import RegisterUseCase


@pytest.mark.asyncio
async def test_register_success(
    register_usecase: RegisterUseCase, register_user_dto: RegisterUserDto
):
    token = await register_usecase(dto=register_user_dto)

    attrs = ("fullname", "email")
    for attr in attrs:
        assert getattr(token.user, attr) == getattr(register_user_dto, attr)
