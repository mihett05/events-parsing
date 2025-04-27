import application.organizations.usecases as usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def create_organization_usecase(
    container: AsyncContainer,
) -> usecases.CreateOrganizationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.CreateOrganizationUseCase)


@pytest_asyncio.fixture
async def read_organization_usecase(
    container: AsyncContainer,
) -> usecases.ReadOrganizationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadOrganizationUseCase)


@pytest_asyncio.fixture
async def readall_organization_usecase(
    container: AsyncContainer,
) -> usecases.ReadAllOrganizationUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadAllOrganizationUseCase)


@pytest_asyncio.fixture
async def update_organization_usecase(container: AsyncContainer):
    async with container() as nested:
        yield await nested.get(usecases.UpdateOrganizationUseCase)


@pytest_asyncio.fixture
async def delete_organization_usecase(container: AsyncContainer):
    async with container() as nested:
        yield await nested.get(usecases.DeleteOrganizationUseCase)
