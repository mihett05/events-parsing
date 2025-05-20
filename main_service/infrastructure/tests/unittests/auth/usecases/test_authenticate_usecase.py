from typing import Any, Callable, Coroutine

import pytest
from application.auth.dtos import AuthenticateUserDto
from application.auth.exceptions import InvalidCredentialsError
from application.auth.usecases import AuthenticateUseCase
from domain.users.entities import UserActivationToken


@pytest.mark.asyncio
async def test_authenticate_success(
    create_user1: UserActivationToken,
    authenticate_user1_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    create_user1 = await create_user1()
    user = await authenticate_usecase(authenticate_user1_dto)
    print(type(create_user1))
    assert user.email == create_user1.email
    assert user.fullname == create_user1.fullname
    assert user.id == create_user1.id


@pytest.mark.asyncio
async def test_authenticate_wrong_password(
    create_user1: UserActivationToken,
    authenticate_user1_broken_password_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    create_user1 = await create_user1()
    with pytest.raises(InvalidCredentialsError) as ex:
        await authenticate_usecase(authenticate_user1_broken_password_dto)
    assert str(ex.value) == str(InvalidCredentialsError("password"))


@pytest.mark.asyncio
async def test_authenticate_user_not_found(
    authenticate_user1_dto: AuthenticateUserDto,
    authenticate_usecase: AuthenticateUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        await authenticate_usecase(authenticate_user1_dto)
    assert str(ex.value) == str(InvalidCredentialsError("email"))
