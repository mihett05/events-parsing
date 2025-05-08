from uuid import UUID

from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User

from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)


class UpdateOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        read_use_case: ReadOrganizationTokenUseCase,
    ):
        self.__repository = repository
        self.__read_use_case = read_use_case

    async def __call__(self, token_id: UUID, actor: User) -> OrganizationToken:
        token = await self.__read_use_case(
            token_id, User(id=0, email="", fullname="")
        )
        token.used_by = actor.id
        token.is_used = True
        return await self.__repository.update(token)
