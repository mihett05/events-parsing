import os
from typing import BinaryIO, Iterable

import pytest_asyncio
from application.attachments.gateways import FilesGateway
from dishka import AsyncContainer
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository


@pytest_asyncio.fixture
async def create_attachment_content() -> Iterable[BinaryIO]:
    test_file_name = "new_file.txt"
    with open(test_file_name, "wb") as file:
        file.write(b"<3")
    with open(test_file_name, "rb") as file:
        yield file
    os.remove(test_file_name)


@pytest_asyncio.fixture
async def create_attachment_dtos(
    create_attachment_content: BinaryIO,
) -> list[CreateAttachmentDto]:
    return [
        CreateAttachmentDto(
            filename=f"лето-2012-анапа({i})",
            extension=".txt",
            content=create_attachment_content,
        )
        for i in range(1, 10)
    ]


@pytest_asyncio.fixture
async def attachments_repository(
    container: AsyncContainer,
) -> AttachmentsRepository:
    async with container() as nested:
        yield await nested.get(AttachmentsRepository)


@pytest_asyncio.fixture
async def files_gateway(container: AsyncContainer) -> FilesGateway:
    async with container() as nested:
        yield await nested.get(FilesGateway)


@pytest_asyncio.fixture
async def create_attachment(
    attachments_repository: AttachmentsRepository,
    create_attachment_dtos: list[CreateAttachmentDto],
    files_gateway: FilesGateway,
    create_attachment_content: BinaryIO,
) -> Attachment:
    attachment = await attachments_repository.create(create_attachment_dtos[0])
    await files_gateway.create(attachment, create_attachment_content)
    return attachment
