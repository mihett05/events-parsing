from typing import Annotated

from dishka import FromDishka
from fastapi import Cookie, Depends
from fastapi.security import (
    APIKeyCookie,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from application.auth.tokens.dtos import TokenInfo
from application.auth.tokens.gateways import TokensGateway

REFRESH_COOKIE = "refresh"
cookie_scheme = APIKeyCookie(name=REFRESH_COOKIE)
oauth2_scheme = OAuth2PasswordBearer("/auth/token")
http_scheme = HTTPBearer()


async def extract_access_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(http_scheme)],
    tokens_gateway: FromDishka[TokensGateway],
) -> TokenInfo:
    return await tokens_gateway.extract_token_info(token.credentials)


async def extract_refresh_token(
    tokens_gateway: FromDishka[TokensGateway],
    cookie: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)],
) -> TokenInfo:
    return await tokens_gateway.extract_token_info(cookie)
