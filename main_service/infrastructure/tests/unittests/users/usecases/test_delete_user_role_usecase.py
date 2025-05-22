import pytest
from application.users.usecases import (
    DeleteUserRoleUseCase,
    ReadUserRoleUseCase,
)
from domain.users.entities import User
from domain.users.exceptions import UserRoleNotFoundError



@pytest.mark.asyncio
async def delete_user_success(
    read_user_role_usecase: ReadUserRoleUseCase,
    delete_user_role_usecase: DeleteUserRoleUseCase,
    delete_user_role_dto,
    get_actor: User,
):
    role = await read_user_role_usecase(
        delete_user_role_dto.user_id, delete_user_role_dto.organization_id
    )
    deleted_role = await delete_user_role_usecase(
        delete_user_role_dto, get_actor
    )
    assert deleted_role == role

    with pytest.raises(UserRoleNotFoundError):
        await read_user_role_usecase(
            delete_user_role_dto.user_id, delete_user_role_dto.organization_id
        )
