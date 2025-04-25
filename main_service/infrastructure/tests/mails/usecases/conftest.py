import application.mails.usecases as usecases
import pytest_asyncio
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def create_mail_usecase(
    container: AsyncContainer,
) -> usecases.CreateMailUseCase:
    async with container() as nested:
        yield await nested.get(usecases.CreateMailUseCase)


@pytest_asyncio.fixture
async def read_mail_usecase(
    container: AsyncContainer,
) -> usecases.ReadMailUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadMailUseCase)


@pytest_asyncio.fixture
async def update_mail_usecase(
    container: AsyncContainer,
) -> usecases.UpdateMailUseCase:
    async with container() as nested:
        yield await nested.get(usecases.UpdateMailUseCase)


@pytest_asyncio.fixture
async def read_unprocessed_mails_usecase(
    container: AsyncContainer,
) -> usecases.ReadUnprocessedMailUseCase:
    async with container() as nested:
        yield await nested.get(usecases.ReadUnprocessedMailUseCase)
