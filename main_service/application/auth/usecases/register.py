from application.auth.tokens.dtos import TokenPairDto
from domain.users.dtos import CreateUserDto
from domain.users.entities import User

from ...users.usecases import CreateUserUseCase
from ..tokens.gateways import SecurityGateway, TokensGateway


class RegisterUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        security_gateway: SecurityGateway,
        token_gateway: TokensGateway,
    ):
        self.token_gateway = token_gateway
        self.security_gateway = security_gateway
        self.create_user_use_case = create_user_use_case

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
        return user, await self.token_gateway.create_token_pair(user.email)
