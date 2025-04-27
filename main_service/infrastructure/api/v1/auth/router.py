from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from application.auth.tokens.dtos import TokenInfoDto, TokenPairDto
from application.auth.usecases import (
    AuthorizeUseCase,
    CreateTokenPairUseCase,
    RegisterUseCase,
)
from application.auth.usecases.login import LoginUseCase
from domain.users.entities import User
from infrastructure.api.v1.auth.deps import extract_refresh_token
from infrastructure.api.v1.auth.dtos import (
    AuthenticateUserModelDto,
    CreateUserModelDto,
)
from infrastructure.api.v1.auth.mappers import (
    map_authenticate_dto_from_pydantic,
    map_create_dto_from_pydantic,
)
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.mappers import map_to_pydantic

router = APIRouter(route_class=DishkaRoute, tags=["Auth"])
REFRESH_COOKIE = "refresh"


def __make_response(user: User, tokens_pair: TokenPairDto):
    response = JSONResponse(
        content=UserWithTokenModel(
            user=map_to_pydantic(user),
            access_token=tokens_pair.access_token,
        ).model_dump(by_alias=True, mode="json"),
    )
    response.set_cookie(REFRESH_COOKIE, tokens_pair.refresh_token)
    return response


@router.post("/login", response_model=UserWithTokenModel)
async def login_user(
    auth_data: AuthenticateUserModelDto,
    login_use_case: FromDishka[LoginUseCase],
):
    user, tokens_pair = await login_use_case(
        map_authenticate_dto_from_pydantic(auth_data)
    )

    return __make_response(user, tokens_pair)


@router.post("/register", response_model=UserWithTokenModel)
async def register_user(
    dto: CreateUserModelDto,
    register_use_case: FromDishka[RegisterUseCase],
):
    user, tokens_pair = await register_use_case(
        map_create_dto_from_pydantic(dto)
    )

    return __make_response(user, tokens_pair)


@router.post("/refresh", response_model=UserWithTokenModel)
async def refresh_token(
    token_info: Annotated[TokenInfoDto, Depends(extract_refresh_token)],
    authorize_use_case: FromDishka[AuthorizeUseCase],
    create_token_pair_use_case: FromDishka[CreateTokenPairUseCase],
):
    user = await authorize_use_case(token_info)
    tokens_pair = await create_token_pair_use_case(user)

    return __make_response(user, tokens_pair)
