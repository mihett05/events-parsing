from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfoDto
from domain.users.entities import User
from domain.users.exceptions import UserNotFoundError
from domain.users.repositories import UsersRepository


class AuthorizeUseCase:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def __call__(self, dto: TokenInfoDto) -> User:
        try:
            return await self.users_repository.read_by_email(dto.subject)
        except UserNotFoundError:
            raise InvalidCredentialsError("email")
