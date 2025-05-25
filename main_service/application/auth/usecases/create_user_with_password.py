from domain.users.entities import User
from domain.users.repositories import UsersRepository

from ..dtos import CreateUserWithPasswordDto, RegisterUserDto
from ..tokens.gateways import SecurityGateway


class CreateUserWithPasswordUseCase:
    def __init__(
        self,
        users_repository: UsersRepository,
        security_gateway: SecurityGateway,
    ):
        self.__repository = users_repository
        self.__security_gateway = security_gateway

    async def __call__(self, dto: RegisterUserDto) -> User:
        password_dto = self.__security_gateway.create_hashed_password(dto.password)
        dto = CreateUserWithPasswordDto(
            email=dto.email,
            fullname=dto.fullname,
            is_active=False,
            salt=password_dto.salt,
            hashed_password=password_dto.hashed_password,
        )

        return await self.__repository.create(dto)
