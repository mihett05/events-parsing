from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError
from domain.users.repositories import UsersRepository

from application.auth.dtos import AuthenticateUserDto
from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import PasswordDto
from application.auth.tokens.gateways import SecurityGateway


class AuthenticateUseCase:
    def __init__(
        self,
        security_gateway: SecurityGateway,
        users_repository: UsersRepository,
    ):
        self.security_gateway = security_gateway
        self.users_repository = users_repository

    async def __call__(self, dto: AuthenticateUserDto) -> User:
        try:
            user = await self.users_repository.read_by_email(dto.email)
            is_password_valid = self.security_gateway.verify_passwords(
                dto.password,
                PasswordDto(hashed_password=user.hashed_password, salt=user.salt),
            )
            if not is_password_valid:
                raise InvalidCredentialsError("password")
            return user
        except UserNotFoundError:
            raise InvalidCredentialsError("email")
