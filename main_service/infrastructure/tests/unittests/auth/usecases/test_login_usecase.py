from typing import Any, Callable, Coroutine

import pytest
from application.auth.dtos import AuthenticateUserDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import LoginUseCase
from domain.users.entities import UserActivationToken


@pytest.mark.asyncio
async def test_login_success(
    create_user1: UserActivationToken,
    authenticate_user1_dto: AuthenticateUserDto,
    login_usecase: LoginUseCase,
    token_gateway: TokensGateway,
):
    create_user1 = await create_user1()

    test_user, _ = await login_usecase(authenticate_user1_dto)
    attrs = ("fullname", "email", "id")
    for attr in attrs:
        assert getattr(test_user, attr) == getattr(create_user1, attr)
