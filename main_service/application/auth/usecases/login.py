from application.auth.tokens.dtos import TokenPairDto
from domain.users.entities import User

from ..dtos import AuthenticateUserDto
from .authenticate import AuthenticateUseCase
from .create_token_pair import CreateTokenPairUseCase


class LoginUseCase:
    def __init__(
        self,
        authenticate_user_use_case: AuthenticateUseCase,
        create_token_pair_use_case: CreateTokenPairUseCase,
    ):
        self.authenticate_user_use_case = authenticate_user_use_case
        self.create_token_pair_use_case = create_token_pair_use_case

    async def __call__(
        self, dto: AuthenticateUserDto
    ) -> tuple[User, TokenPairDto]:
        user = await self.authenticate_user_use_case(dto)
        return user, await self.create_token_pair_use_case(user)
