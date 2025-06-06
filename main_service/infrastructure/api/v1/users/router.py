from typing import Annotated

import application.users.usecases as use_cases
from aiogram import Bot
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.users.dtos import ReadAllUsersDto
from domain.users.entities import User
from fastapi import APIRouter, Depends

import infrastructure.api.v1.users.dtos as dtos
import infrastructure.api.v1.users.mappers as mappers
import infrastructure.api.v1.users.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user
from infrastructure.api.v1.users.dtos import CreateUserRoleModelDto

router = APIRouter(route_class=DishkaRoute, tags=["Users"])


@router.get("/", response_model=list[models.UserModel])
async def read_all_users(
    use_case: FromDishka[use_cases.ReadAllUsersUseCase],
    page: int = 0,
    page_size: int = 50,
):
    """Получает список пользователей с пагинацией.

    По умолчанию возвращает первые 50 пользователей.
    """
    return map(
        mappers.map_to_pydantic,
        await use_case(ReadAllUsersDto(page=page, page_size=page_size)),
    )


@router.get("/me", response_model=models.UserModel)
async def get_me(user: Annotated[User, Depends(get_user)]):
    """Возвращает данные текущего аутентифицированного пользователя."""

    return mappers.map_to_pydantic(user)


@router.get(
    "/{user_id}",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def read_user(user_id: int, use_case: FromDishka[use_cases.ReadUserUseCase]):
    """Получает данные пользователя по его ID."""

    return mappers.map_to_pydantic(await use_case(user_id))


@router.put(
    "/me",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def update_user(
    dto: dtos.UpdateUserModelDto,
    actor: Annotated[User, Depends(get_user)],
    use_case: FromDishka[use_cases.UpdateUserUseCase],
):
    """Обновляет данные текущего пользователя."""

    return mappers.map_to_pydantic(
        await use_case(mappers.map_update_dto_from_pydantic(dto, actor.id), actor)
    )


@router.delete(
    "/",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_user(
    use_case: FromDishka[use_cases.DeleteUserUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаляет текущего пользователя."""

    return mappers.map_to_pydantic(await use_case(actor))


@router.post("/telegram")
async def create_telegram_link(
    bot: FromDishka[Bot],
    use_case: FromDishka[use_cases.CreateTelegramTokenUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Создает ссылку для привязки Telegram аккаунта."""

    return await use_case((await bot.get_me()).username, actor)


@router.get(
    "/roles/{user_id}/{organization_id}",
    response_model=models.UserRoleModel,
    responses={404: {"model": ErrorModel}},
)
async def read_user_role(
    user_id: int,
    organization_id: int,
    use_case: FromDishka[use_cases.ReadUserRoleUseCase],
):
    """Получает роль пользователя в конкретной организации."""

    return mappers.map_role_to_pydantic(await use_case(user_id, organization_id))


@router.get(
    "/roles/{user_id}",
    response_model=list[models.UserRoleModel],
    responses={404: {"model": ErrorModel}},
)
async def read_user_roles(
    user_id: int,
    use_case: FromDishka[use_cases.ReadUserRolesUseCase],
):
    """Получает все роли пользователя во всех организациях."""

    return map(mappers.map_role_to_pydantic, await use_case(user_id))


@router.post(
    "/roles",
    response_model=models.UserRoleModel,
    responses={404: {"model": ErrorModel}},
)
async def create_user_role(
    dto: CreateUserRoleModelDto,
    actor: Annotated[User, Depends(get_user)],
    use_case: FromDishka[use_cases.CreateUserRoleUseCase],
):
    """Создает новую роль пользователя в организации."""

    return mappers.map_role_to_pydantic(
        await use_case(mappers.map_create_role_dto_to_entity(dto), actor)
    )


@router.put(
    "/roles/update",
    response_model=models.UserRoleModel,
    responses={404: {"model": ErrorModel}},
)
async def update_user_role(
    dto: dtos.UpdateUserRoleModelDto,
    actor: Annotated[User, Depends(get_user)],
    use_case: FromDishka[use_cases.UpdateUserRoleUseCase],
):
    """Обновляет роль пользователя в организации."""

    return mappers.map_role_to_pydantic(
        await use_case(mappers.map_update_role_entity_from_pydantic(dto), actor)
    )


@router.delete(
    "/roles/{user_id}/{organization_id}",
    response_model=models.UserRoleModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_user_role(
    user_id: int,
    organization_id: int,
    use_case: FromDishka[use_cases.DeleteUserRoleUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    """Удаляет роль пользователя в организации."""

    return mappers.map_role_to_pydantic(
        await use_case(
            mappers.map_delete_role_to_dto(user_id, organization_id),
            actor,
        )
    )
