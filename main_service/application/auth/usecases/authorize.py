from domain.users.entities import User
from domain.users.exceptions import UserNotFound
from domain.users.repositories import UsersRepository

from application.auth.exceptions import InvalidCredentialsError
from application.auth.tokens.dtos import TokenInfo


class AuthorizeUseCase:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def __call__(self, dto: TokenInfo) -> User:
        try:
            return await self.users_repository.read(dto.subject)
        except UserNotFound:
            raise InvalidCredentialsError()
