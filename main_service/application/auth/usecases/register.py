from application.auth.tokens.dtos import TokenPairDto
from domain.users.dtos import CreateUserDto
from domain.users.entities import User

from ...users.usecases import CreateUserUseCase
from .create_token_pair import CreateTokenPairUseCase


class RegisterUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        create_token_pair_use_case: CreateTokenPairUseCase,
    ):
        self.create_user_use_case = create_user_use_case
        self.create_token_pair_use_case = create_token_pair_use_case

    async def __call__(self, dto: CreateUserDto) -> tuple[User, TokenPairDto]:
        user = await self.create_user_use_case(dto)
        return user, await self.create_token_pair_use_case(user)
