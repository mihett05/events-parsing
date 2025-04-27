import pytest
from application.auth.dtos import RegisterUserDTO
from application.auth.usecases import RegisterUseCase


@pytest.mark.asyncio
async def test_register_success(
    register_usecase: RegisterUseCase, register_user1_dto: RegisterUserDTO
):
    user, _ = await register_usecase(dto=register_user1_dto)

    attrs = ("fullname", "email")
    for attr in attrs:
        assert getattr(user, attr) == getattr(register_user1_dto, attr)
