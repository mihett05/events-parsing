import pytest

from application.auth.tokens.dtos import TokenInfoDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import (
    AuthorizeUseCase,
    CreateTokenPairUseCase,
    LoginUseCase,
)
from domain.users.entities import User
from infrastructure.tests.auth.conftest import token_gateway


# всё ок
@pytest.mark.asyncio
async def test_create_token_pair_success(
    create_user1: User,
    create_token_pair_usecase: CreateTokenPairUseCase,
    token_gateway: TokensGateway,
):
    get_token_pair = await create_token_pair_usecase(create_user1)
    access_token_info = await token_gateway.extract_token_info(
        get_token_pair.access_token
    )
    refresh_token_info = await token_gateway.extract_token_info(
        get_token_pair.refresh_token
    )
    assert access_token_info.subject == create_user1.email
    assert refresh_token_info.subject == create_user1.email
