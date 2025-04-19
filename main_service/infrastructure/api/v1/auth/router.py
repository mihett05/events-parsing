from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from starlette.responses import JSONResponse

from application.auth.usecases import RegisterUseCase
from application.auth.usecases.login import LoginUseCase
from infrastructure.api.v1.auth.dtos import (
    CreateUserModelDto,
    UserAuthenticate,
    UserWithToken,
)
from infrastructure.api.v1.auth.mappers import (
    map_authenticate_dto_from_pydantic,
    map_create_dto_from_pydantic,
)
from infrastructure.api.v1.users.mappers import map_to_pydantic

router = APIRouter(route_class=DishkaRoute, tags=["Auth"])
REFRESH_COOKIE = "refresh"


@router.post("/login", response_model=UserWithToken)
async def login_user(
    auth_data: UserAuthenticate,
    login_use_case: FromDishka[LoginUseCase],
):
    user, tokens_pair = await login_use_case(
        map_authenticate_dto_from_pydantic(auth_data)
    )

    response = JSONResponse(
        content=UserWithToken(
            user=map_to_pydantic(user),
            access_token=tokens_pair.access_token,
        ).model_dump(by_alias=True),
    )
    response.set_cookie(REFRESH_COOKIE, tokens_pair.refresh_token)
    return response


@router.post("/register", response_model=UserWithToken)
async def register_user(
    dto: CreateUserModelDto,
    register_use_case: FromDishka[RegisterUseCase],
):
    user, tokens_pair = await register_use_case(
        map_create_dto_from_pydantic(dto)
    )

    response = JSONResponse(
        content=UserWithToken(
            user=map_to_pydantic(user),
            access_token=tokens_pair.access_token,
        ).model_dump(by_alias=True),
    )
    response.set_cookie(REFRESH_COOKIE, tokens_pair.refresh_token)
    return response
