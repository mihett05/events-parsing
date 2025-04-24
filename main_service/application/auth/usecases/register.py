from domain.users.dtos import CreateUserDto
from domain.users.entities import User

from application.auth.tokens.dtos import TokenPairDto

from ...users.usecases import CreateUserUseCase
from ..tokens.gateways import SecurityGateway
from .create_token_pair import CreateTokenPairUseCase


class RegisterUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        security_gateway: SecurityGateway,
        create_token_pair_use_case: CreateTokenPairUseCase,
    ):
        self.create_user_use_case = create_user_use_case
        self.create_token_pair_use_case = create_token_pair_use_case
        self.security_gateway = security_gateway

    async def __call__(self, dto: CreateUserDto) -> tuple[User, TokenPairDto]:
        password_dto = self.security_gateway.create_hashed_password(
            dto.password
        )
        user = User(
            email=dto.email,
            fullname=dto.fullname,
            salt=password_dto.salt,
            hashed_password=password_dto.hashed_password,
        )

        user = await self.create_user_use_case(user)
        return user, await self.create_token_pair_use_case(user)
