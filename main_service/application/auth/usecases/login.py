from application.auth.tokens.dtos import TokenPairDto
from domain.users.entities import User

from ..dtos import AuthenticateUserDto
from ..tokens.gateways import TokensGateway
from .authenticate import AuthenticateUseCase


class LoginUseCase:
    def __init__(
        self,
        authenticate_user_use_case: AuthenticateUseCase,
        token_gateway: TokensGateway,
    ):
        self.authenticate_user_use_case = authenticate_user_use_case
        self.token_gateway = token_gateway

    async def __call__(
        self, dto: AuthenticateUserDto
    ) -> tuple[User, TokenPairDto]:
        user = await self.authenticate_user_use_case(dto)
        return user, await self.token_gateway.create_token_pair(user.email)
