import os
from datetime import datetime, timedelta, timezone
from typing import Any, BinaryIO, Callable, Coroutine, Iterable

import pytest_asyncio
from application.attachments.gateways import FilesGateway
from application.attachments.usecases import CreateAttachmentUseCase
from dishka import AsyncContainer
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.organizations.entities import Organization
from domain.users.entities import User


@pytest_asyncio.fixture
async def events_repository(container: AsyncContainer) -> EventsRepository:
    async with container() as request_container:
        yield await request_container.get(EventsRepository)


@pytest_asyncio.fixture
async def create_attachment_content() -> Iterable[BinaryIO]:
    test_file_name = "new_file.txt"
    with open(test_file_name, "wb") as file:
        file.write(b"Example data <3")
    with open(test_file_name, "rb") as file:
        yield file
    os.remove(test_file_name)


@pytest_asyncio.fixture
async def create_attachment_dtos(
    create_attachment_content: BinaryIO,
    get_admin_event: Event,
) -> list[CreateAttachmentDto]:
    return [
        CreateAttachmentDto(
            filename=f"лето-2012-анапа({i})",
            extension=".txt",
            content=create_attachment_content,
            event=get_admin_event,
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
async def create_attachment_usecase(
    container: AsyncContainer,
) -> CreateAttachmentDto:
    async with container() as nested:
        yield await nested.get(CreateAttachmentUseCase)


@pytest_asyncio.fixture(scope="function")
async def create_attachment(
    get_admin: User,
    create_attachment_dtos: list[CreateAttachmentDto],
    create_attachment_usecase: CreateAttachmentUseCase,
) -> Attachment:
    succeed, _ = await create_attachment_usecase([create_attachment_dtos[0]], get_admin)
    return succeed[0]
