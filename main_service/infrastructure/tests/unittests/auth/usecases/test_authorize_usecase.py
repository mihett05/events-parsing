from typing import Any, Callable, Coroutine

import pytest
from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.usecases import AuthorizeUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_authorize_success(
    create_user1: Callable[[], Coroutine[Any, Any, User]],
    user1_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    create_user1 = await create_user1()

    user = await authorize_usecase(user1_token_info_dto)
    attrs = ("fullname", "email", "id")
    for attr in attrs:
        assert getattr(user, attr) == getattr(create_user1, attr)


@pytest.mark.asyncio
async def test_authorize_user_not_found(
    create_user1: Callable[[], Coroutine[Any, Any, User]],
    user2_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    create_user1 = await create_user1()

    with pytest.raises(InvalidCredentialsError) as ex:
        await authorize_usecase(user2_token_info_dto)
    assert str(ex.value) == str(InvalidCredentialsError("email"))
