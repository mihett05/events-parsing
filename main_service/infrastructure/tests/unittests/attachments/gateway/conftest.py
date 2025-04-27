import pytest_asyncio
from application.attachments.gateways import FilesGateway
from application.attachments.usecases import ReadAttachmentUseCase
from dishka import AsyncContainer


@pytest_asyncio.fixture
async def files_gateway(
    container: AsyncContainer,
) -> FilesGateway:
    async with container() as nested:
        yield await nested.get(FilesGateway)


@pytest_asyncio.fixture
async def read_attachment_usecase(
    container: AsyncContainer,
) -> ReadAttachmentUseCase:
    async with container() as nested:
        yield await nested.get(ReadAttachmentUseCase)
