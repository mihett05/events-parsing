from abc import ABCMeta, abstractmethod
from uuid import UUID

import domain.organizations.dtos as dtos
import domain.organizations.entities as entities


class OrganizationsRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(
        self, dto: dtos.CreateOrganizationDto
    ) -> entities.Organization: ...

    @abstractmethod
    async def read(self, id_: int) -> entities.Organization: ...

    @abstractmethod
    async def read_all(
        self, dto: dtos.ReadOrganizationsDto
    ) -> list[entities.Organization]: ...

    @abstractmethod
    async def update(
        self, organization: entities.Organization
    ) -> entities.Organization: ...

    @abstractmethod
    async def delete(
        self, organization: entities.Organization
    ) -> entities.Organization: ...


class OrganizationTokensRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(
        self, dto: dtos.CreateOrganizationTokenDto
    ) -> entities.OrganizationToken: ...

    @abstractmethod
    async def read(self, token_id: UUID) -> entities.OrganizationToken: ...

    @abstractmethod
    async def update(
        self, token: entities.OrganizationToken
    ) -> entities.OrganizationToken: ...

    @abstractmethod
    async def delete(
        self, token: entities.OrganizationToken
    ) -> entities.OrganizationToken: ...
