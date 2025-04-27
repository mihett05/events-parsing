from datetime import datetime

import pytest_asyncio
from dishka import AsyncContainer

from application.mails.dtos import UpdateMailDto
from domain.mails.dtos import CreateMailDto, ReadAllMailsDto
from domain.mails.entities import Mail
from domain.mails.enums import MailStateEnum
from domain.mails.repositories import MailsRepository


@pytest_asyncio.fixture
async def create_mail_dto() -> CreateMailDto:
    return CreateMailDto(
        theme="Example",
        sender="example@example.com",
        raw_content="Example Contend".encode("utf-8"),
        received_date=datetime.now().date(),
    )


@pytest_asyncio.fixture
async def update_mail_dto() -> UpdateMailDto:
    return UpdateMailDto(
        id=1,
        state=MailStateEnum.PROCESSED,
    )


@pytest_asyncio.fixture
async def read_all_mails_dto() -> ReadAllMailsDto:
    return ReadAllMailsDto(
        page=0,
        page_size=50,
    )


@pytest_asyncio.fixture
async def mails_repository(container: AsyncContainer) -> MailsRepository:
    yield await container.get(MailsRepository)


@pytest_asyncio.fixture
async def create_mail(
    create_mail_dto: CreateMailDto,
    mails_repository: MailsRepository,
) -> Mail:
    return await mails_repository.create(create_mail_dto)
