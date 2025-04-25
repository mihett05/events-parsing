import pytest

from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto
from application.auth.usecases import AuthorizeUseCase
from domain.users.entities import User


# всё ок
@pytest.mark.asyncio
async def test_authenticate_success(
    create_user1: User,
    user1_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    user = await authorize_usecase(user1_token_info_dto)
    assert user.email == create_user1.email
    assert user.fullname == create_user1.fullname
    assert user.id == create_user1.id


# нет юзера
@pytest.mark.asyncio
async def test_authenticate_user_not_found(
    create_user2: User,
    user1_token_info_dto: TokenInfoDto,
    authorize_usecase: AuthorizeUseCase,
):
    with pytest.raises(InvalidCredentialsError) as ex:
        await authorize_usecase(user1_token_info_dto)
    assert str(ex.value) == str(InvalidCredentialsError("email"))
