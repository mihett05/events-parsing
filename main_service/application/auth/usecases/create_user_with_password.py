from domain.users.entities import User

from application.users.usecases import CreateUserUseCase

from ..dtos import RegisterUserDTO
from ..tokens.gateways import SecurityGateway


class CreateUserWithPasswordUseCase:
    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        security_gateway: SecurityGateway,
    ):
        self.create_user_use_case = create_user_use_case
        self.security_gateway = security_gateway

    async def __call__(self, dto: RegisterUserDTO) -> User:
        password_dto = self.security_gateway.create_hashed_password(dto.password)
        user = User(
            email=dto.email,
            fullname=dto.fullname,
            salt=password_dto.salt,
            hashed_password=password_dto.hashed_password,
            is_active=False,
        )

        return await self.create_user_use_case(user)
