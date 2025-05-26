import pytest
from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.usecases import AuthorizeUseCase
from domain.users.entities import User


@pytest.mark.asyncio
async def test_authorize_success(
    get_user_entity: User,
    get_user_authorize_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    user = await authorize_usecase(get_user_authorize_token_info_dto)
    attrs = ("fullname", "email", "id")
    for attr in attrs:
        assert getattr(user, attr) == getattr(get_user_entity, attr)


@pytest.mark.asyncio
async def test_authorize_user_not_found(
    get_user_authorize_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        get_user_authorize_token_info_dto.subject = "example@example.com"
        await authorize_usecase(get_user_authorize_token_info_dto)

    assert str(ex.value) == str(InvalidCredentialsError("email"))
