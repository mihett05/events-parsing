from typing import Annotated

import application.users.usecases as use_cases
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
    return map(
        mappers.map_to_pydantic,
        await use_case(ReadAllUsersDto(page=page, page_size=page_size)),
    )


@router.get("/me", response_model=models.UserModel)
async def get_me(user: Annotated[User, Depends(get_user)]):
    return mappers.map_to_pydantic(user)


@router.get(
    "/{user_id}",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def read_user(
    user_id: int, use_case: FromDishka[use_cases.ReadUserUseCase]
):
    return mappers.map_to_pydantic(await use_case(user_id))


@router.put(
    "/{user_id}",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def update_user(
    user_id: int,
    dto: dtos.UpdateUserModelDto,
    actor: Annotated[User, Depends(get_user)],
    use_case: FromDishka[use_cases.UpdateUserUseCase],
):
    return mappers.map_to_pydantic(
        await use_case(
            mappers.map_update_dto_from_pydantic(dto, user_id), actor
        )
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
    return mappers.map_to_pydantic(await use_case(actor))


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
    return mappers.map_role_to_pydantic(
        await use_case(user_id, organization_id)
    )


@router.get(
    "/roles/{user_id}",
    response_model=list[models.UserRoleModel],
    responses={404: {"model": ErrorModel}},
)
async def read_user_roles(
    user_id: int,
    use_case: FromDishka[use_cases.ReadUserRolesUseCase],
):
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
    return mappers.map_role_to_pydantic(
        await use_case(
            mappers.map_delete_role_to_dto(user_id, organization_id),
            actor,
        )
    )
