import pytest
from application.auth.dtos import RegisterUserDto
from application.auth.usecases import RegisterUseCase
from application.users.usecases import DeleteUserUseCase, ReadUserUseCase
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError


@pytest.mark.asyncio
async def delete_user_success(
    read_user_usecase: ReadUserUseCase,
    delete_user_usecase: DeleteUserUseCase,
    register_user_usecase: RegisterUseCase,
    register_user1_dto: RegisterUserDto,
):
    token = await register_user_usecase(dto=register_user1_dto)
    deleted_user = await delete_user_usecase(token.user)
    assert deleted_user == token.user

    with pytest.raises(UserNotFoundError):
        await read_user_usecase(token.user.id)


@pytest.mark.asyncio
async def test_delete_not_found(
    delete_user_usecase: DeleteUserUseCase, get_user_entity: User
):
    await delete_user_usecase(get_user_entity)
    with pytest.raises(UserNotFoundError):
        await delete_user_usecase(get_user_entity)
