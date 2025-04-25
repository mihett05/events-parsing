import pytest_asyncio
from dishka import AsyncContainer

from application.attachments.usecases import (
    CreateAttachmentUseCase,
    DeleteAttachmentUseCase,
    ReadAttachmentUseCase,
)
from domain.attachments.dtos import CreateAttachmentDto


@pytest_asyncio.fixture
async def create_attachment_usecase(
    container: AsyncContainer,
) -> CreateAttachmentDto:
    async with container() as nested:
        yield await nested.get(CreateAttachmentUseCase)


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
