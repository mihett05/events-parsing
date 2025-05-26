from typing import Any, Callable, Coroutine

import pytest
from application.auth.dtos import AuthenticateUserDto
from application.auth.exceptions import InvalidCredentialsError
from application.auth.usecases import AuthenticateUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_authenticate_success(
    get_user_entity: User,
    get_user_authenticate_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    user = await authenticate_usecase(get_user_authenticate_dto)

    assert user.id == get_user_entity.id
    assert user.email == get_user_entity.email
    assert user.fullname == get_user_entity.fullname


@pytest.mark.asyncio
async def test_authenticate_wrong_password(
    get_user_entity: User,  # noqa
    get_user_authenticate_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        get_user_authenticate_dto.password = "Aliboba"
        await authenticate_usecase(get_user_authenticate_dto)

    assert str(ex.value) == str(InvalidCredentialsError("password"))


@pytest.mark.asyncio
async def test_authenticate_user_not_found(
    get_user_entity: User,  # noqa
    get_user_authenticate_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        get_user_authenticate_dto.email = "example@example.com"
        await authenticate_usecase(get_user_authenticate_dto)
    assert str(ex.value) == str(InvalidCredentialsError("email"))
