from typing import Any, Callable, Coroutine

import application.auth.usecases
import pytest
from application.auth.tokens.gateways import TokensGateway
from domain.users.entities import User


@pytest.mark.asyncio
async def test_create_token_pair_success(
    get_user_entity: User,
    create_token_pair_usecase: application.auth.usecases.CreateTokenPairUseCase,
    token_gateway: TokensGateway,
):
    get_token_pair = await create_token_pair_usecase(get_user_entity)
    access_token_info = await token_gateway.extract_token_info(
        get_token_pair.access_token
    )
    refresh_token_info = await token_gateway.extract_token_info(
        get_token_pair.refresh_token
    )
    assert access_token_info.subject == get_user_entity.email
    assert refresh_token_info.subject == get_user_entity.email
