from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

import application.users.usecases as use_cases
import infrastructure.api.v1.users.dtos as dtos
import infrastructure.api.v1.users.mappers as mappers
import infrastructure.api.v1.users.models as models
from domain.users.dtos import ReadAllUsersDto
from infrastructure.api.models import ErrorModel

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
    use_case: FromDishka[use_cases.UpdateUserUseCase],
):
    return mappers.map_to_pydantic(
        await use_case(mappers.map_update_dto_from_pydantic(dto, user_id), None)
    )


@router.delete(
    "/{user_id}",
    response_model=models.UserModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_user(
    user_id: int,
    use_case: FromDishka[use_cases.DeleteUserUseCase],
):
    return mappers.map_to_pydantic(await use_case(user_id, None))
