from datetime import datetime, timedelta, timezone

import jwt
from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.config import TokenConfig
from application.auth.tokens.dtos import TokenInfoDto, TokenPairDto
from application.auth.tokens.gateways import TokensGateway


class JwtTokensGateway(TokensGateway):
    def __init__(self, config: TokenConfig):
        self.__config = config

    def __encode(self, subject: str, expires_time: timedelta | None = None) -> str:
        payload = {"sub": subject} | (
            {"exp": datetime.now(tz=timezone.utc) + expires_time}
            if expires_time
            else dict()
        )
        return jwt.encode(
            payload,
            key=self.__config.secret_key,
            algorithm=self.__config.algorithm,
        )

    async def create_token_pair(self, subject: str) -> TokenPairDto:
        access_token = self.__encode(subject, self.__config.access_token_expires_time)
        refresh_token = self.__encode(subject, self.__config.refresh_token_expires_time)
        return TokenPairDto(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def extract_token_info(
        self, token: str, check_expires: bool = True
    ) -> TokenInfoDto:
        try:
            payload = jwt.decode(
                token,
                key=self.__config.secret_key,
                algorithms=[self.__config.algorithm],
                options={"verify_signature": check_expires},
            )
        except jwt.ExpiredSignatureError:
            raise InvalidCredentialsError()
        return TokenInfoDto(
            subject=payload["sub"],
            expires_in=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )
