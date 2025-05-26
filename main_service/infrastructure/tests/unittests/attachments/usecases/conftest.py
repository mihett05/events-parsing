import pytest_asyncio
from application.attachments.usecases import (
    CreateAttachmentUseCase,
    DeleteAttachmentUseCase,
    ReadAttachmentUseCase,
)
from dishka import AsyncContainer
from domain.attachments.dtos import CreateAttachmentDto


@pytest_asyncio.fixture
async def delete_attachment_usecase(
    container: AsyncContainer,
) -> DeleteAttachmentUseCase:
    async with container() as nested:
        yield await nested.get(DeleteAttachmentUseCase)


@pytest_asyncio.fixture
async def read_attachment_usecase(
    container: AsyncContainer,
) -> ReadAttachmentUseCase:
    async with container() as nested:
        yield await nested.get(ReadAttachmentUseCase)
