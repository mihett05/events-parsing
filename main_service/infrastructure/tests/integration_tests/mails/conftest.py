import datetime
import os
from io import BytesIO
from typing import BinaryIO

import pytest_asyncio
from application.mails.gateway import EmailsGateway
from dishka import AsyncContainer
from domain.attachments.dtos import CreateAttachmentDto, ParsedAttachmentInfoDto
from domain.mails.dtos import ParsedMailInfoDto

from infrastructure.config import Config
from infrastructure.gateways.notifications.gateways import NotificationEmailGateway


@pytest_asyncio.fixture
async def notification_email_gateway(
    container: AsyncContainer,
) -> NotificationEmailGateway:
    return await container.get(NotificationEmailGateway)


@pytest_asyncio.fixture
async def imap_email_gateway(
    container: AsyncContainer,
) -> EmailsGateway:
    return await container.get(EmailsGateway)


@pytest_asyncio.fixture
async def get_config(
    container: AsyncContainer,
) -> Config:
    return await container.get(Config)


@pytest_asyncio.fixture
async def create_attachment_content() -> BinaryIO:
    test_file_name = "new_file.txt"
    with open(test_file_name, "wb") as file:
        file.write(b"<3")
    with open(test_file_name, "rb") as file:
        file_bytes = file.read()
    os.remove(test_file_name)
    return BytesIO(file_bytes)


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
async def create_mails(
    create_attachment_content: BinaryIO, get_config: Config
) -> list[ParsedMailInfoDto]:
    return [
        ParsedMailInfoDto(
            imap_mail_uid=f"{i}",
            theme="Уведомление",
            sender=get_config.imap_username,
            raw_content=f"hello{i}".encode("utf-8"),
            attachments=[
                ParsedAttachmentInfoDto(
                    filename=f"лето-2012-анапа({i})",
                    extension=".txt",
                    content=create_attachment_content,
                )
            ],
            received_date=datetime.date.today(),
        )
        for i in range(2)
    ]
