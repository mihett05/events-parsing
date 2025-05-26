from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError, UserNotValidated
from domain.users.repositories import UsersRepository

from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto


class AuthorizeUseCase:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def __call__(self, dto: TokenInfoDto) -> User:
        try:
            if user := await self.users_repository.read_by_email(dto.subject):
                if user.is_active:
                    return user
                raise UserNotValidated
        except UserNotFoundError:
            raise InvalidCredentialsError("email")
