import os
from datetime import datetime
from typing import Any, BinaryIO, Callable, Coroutine, Iterable

import pytest
import pytest_asyncio
from application.attachments.gateways import FilesGateway
from dishka import AsyncContainer
from domain.attachments.dtos import CreateAttachmentDto
from domain.attachments.entities import Attachment
from domain.attachments.repositories import AttachmentsRepository
from domain.mails.dtos import CreateMailDto
from domain.mails.entities import Mail
from domain.mails.repositories import MailsRepository


@pytest_asyncio.fixture
async def create_mail_dto() -> CreateMailDto:
    return CreateMailDto(
        imap_mail_uid="example",
        theme="Example",
        sender="example@example.com",
        raw_content="Example Contend".encode("utf-8"),
        received_date=datetime.now().date(),
    )


@pytest_asyncio.fixture
async def mails_repository(container: AsyncContainer) -> MailsRepository:
    async with container() as request_container:
        yield await request_container.get(MailsRepository)


@pytest_asyncio.fixture
async def create_mail(
    create_mail_dto: CreateMailDto,
    mails_repository: MailsRepository,
) -> Mail:
    return await mails_repository.create(create_mail_dto)


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
    create_mail: Mail,
) -> list[CreateAttachmentDto]:
    return [
        CreateAttachmentDto(
            filename=f"лето-2012-анапа({i})",
            extension=".txt",
            content=create_attachment_content,
            mail=create_mail,
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


@pytest_asyncio.fixture(scope="function")
async def create_attachment(
    attachments_repository: AttachmentsRepository,
    create_attachment_dtos: list[CreateAttachmentDto],
    files_gateway: FilesGateway,
    create_attachment_content: BinaryIO,
) -> Callable[..., Coroutine[Any, Any, Attachment]]:
    async def _factory():
        attachment = await attachments_repository.create(create_attachment_dtos[0])
        await files_gateway.create(attachment, create_attachment_content)
        return attachment

    return _factory


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare(
    pytestconfig: pytest.Config,
    attachments_repository: AttachmentsRepository,
    mails_repository: MailsRepository,
):
    if pytestconfig.getoption("--integration", default=False):
        return
    await attachments_repository.clear()  # noqa
    await mails_repository.clear()  # noqa
