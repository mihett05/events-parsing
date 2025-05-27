from typing import Annotated

from application.auth.tokens.dtos import TokenInfoDto
from application.auth.tokens.gateways import TokensGateway
from application.auth.usecases import AuthorizeUseCase
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from domain.users.entities import User
from fastapi import Cookie, Depends
from fastapi.security import (
    APIKeyCookie,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

REFRESH_COOKIE = "refresh"
cookie_scheme = APIKeyCookie(name=REFRESH_COOKIE)
oauth2_scheme = OAuth2PasswordBearer("/auth/token")
http_scheme = HTTPBearer()


@inject
async def extract_access_token(
    tokens_gateway: FromDishka[TokensGateway],
    token: Annotated[HTTPAuthorizationCredentials, Depends(http_scheme)],
) -> TokenInfoDto:
    """Извлекает и валидирует информацию из access-токена."""

    return await tokens_gateway.extract_token_info(token.credentials)


@inject
async def extract_refresh_token(
    tokens_gateway: FromDishka[TokensGateway],
    cookie: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)],
) -> TokenInfoDto:
    """Извлекает и валидирует информацию из refresh-токена, полученного из куки."""

    return await tokens_gateway.extract_token_info(cookie)


@inject
async def get_user(
    token: Annotated[TokenInfoDto, Depends(extract_access_token)],
    authorize_use_case: FromDishka[AuthorizeUseCase],
) -> User:
    """Возвращает аутентифицированного пользователя на основе access-токена."""

    return await authorize_use_case(token)
