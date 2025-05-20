import pytest
from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.usecases import AuthorizeUseCase
from domain.users.entities import UserActivationToken


@pytest.mark.asyncio
async def test_authenticate_success(
    create_user1: UserActivationToken,
    user1_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    user = await authorize_usecase(user1_token_info_dto)
    attrs = ("fullname", "email", "id")
    for attr in attrs:
        assert getattr(user, attr) == getattr(create_user1.user, attr)


@pytest.mark.asyncio
async def test_authenticate_user_not_found(
    create_user2: UserActivationToken,
    user1_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        await authorize_usecase(user1_token_info_dto)
    assert str(ex.value) == str(InvalidCredentialsError("email"))
