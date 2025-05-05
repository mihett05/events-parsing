from datetime import datetime

import pytest
import pytest_asyncio
from application.organizations.dtos import UpdateOrganizationDto
from dishka import AsyncContainer
from domain.organizations.dtos import (
    CreateOrganizationDto,
    ReadOrganizationsDto,
)
from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository


@pytest_asyncio.fixture
async def create_organization_dto() -> CreateOrganizationDto:
    date = datetime.now().now()
    return CreateOrganizationDto(
        title="Test Organization", created_at=date, owner_id=1
    )


@pytest_asyncio.fixture
async def organizations_repository(
    container: AsyncContainer,
) -> OrganizationsRepository:
    async with container() as request_container:
        yield await request_container.get(OrganizationsRepository)


@pytest_asyncio.fixture
async def readall_organizations_dto() -> ReadOrganizationsDto:
    return ReadOrganizationsDto(page=0, page_size=50)


@pytest_asyncio.fixture
async def update_organization_dto() -> UpdateOrganizationDto:
    return UpdateOrganizationDto(id=1, title="Bombordillo crocodillo")


@pytest_asyncio.fixture
async def create_organization(
    create_organization_dto: CreateOrganizationDto,
    organizations_repository: OrganizationsRepository,
) -> Organization:
    return await organizations_repository.create(create_organization_dto)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    organizations_repository: OrganizationsRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await organizations_repository.clear()  # noqa
