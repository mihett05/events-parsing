import pytest

from application.auth.dtos import AuthenticateUserDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import LoginUseCase
from domain.users.entities import User


# всё ок
@pytest.mark.asyncio
async def test_login_success(
    create_user1: User,
    authenticate_user1_dto: AuthenticateUserDto,
    login_usecase: LoginUseCase,
    token_gateway: TokensGateway,
):
    test_user, test_token_pair_dto = await login_usecase(authenticate_user1_dto)
    assert test_user.fullname == create_user1.fullname
    assert test_user.email == create_user1.email
    assert test_user.id == create_user1.id

    access_token_info = await token_gateway.extract_token_info(
        test_token_pair_dto.access_token
    )
    refresh_token_info = await token_gateway.extract_token_info(
        test_token_pair_dto.refresh_token
    )
    assert access_token_info.subject == create_user1.email
    assert refresh_token_info.subject == create_user1.email
