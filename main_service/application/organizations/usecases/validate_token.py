from uuid import UUID

from domain.organizations.exceptions import OrganizationTokenNotFoundError
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User

from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)


class ValidateOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        read_use_case: ReadOrganizationTokenUseCase,
        super_user: User,
    ):
        self.__repository = repository
        self.__read_use_case = read_use_case
        self.__super_user = super_user

    async def __call__(self, token_id: UUID, actor: User) -> bool:
        try:
            token = await self.__read_use_case(token_id, self.__super_user)
            return not token.is_used
        except OrganizationTokenNotFoundError:
            return False
