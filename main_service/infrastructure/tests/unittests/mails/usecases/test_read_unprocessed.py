from datetime import timedelta
from random import choice

import pytest
from application.mails.usecases import ReadUnprocessedMailUseCase
from domain.mails.dtos import CreateMailDto, ReadAllMailsDto
from domain.mails.enums import MailStateEnum
from domain.mails.repositories import MailsRepository


@pytest.mark.asyncio
async def test_read_organization_mails_success(
    read_unprocessed_mails_usecase: ReadUnprocessedMailUseCase,
    read_all_mails_dto: ReadAllMailsDto,
    mails_repository: MailsRepository,
    create_mail_dto: CreateMailDto,
):
    data = []
    count = 0
    theme = create_mail_dto.theme
    for i in range(10):
        create_mail_dto.theme = f"{theme}_{i}"
        create_mail_dto.retry_after -= timedelta(days=10)
        create_mail_dto.state = choice(
            [MailStateEnum.UNPROCESSED, MailStateEnum.PROCESSED]
        )
        count += create_mail_dto.state == MailStateEnum.UNPROCESSED

        mail = await mails_repository.create(create_mail_dto)
        print(type(mails_repository))
        if create_mail_dto.state == MailStateEnum.UNPROCESSED:
            print(mail)
            print()
            if mail.state == MailStateEnum.UNPROCESSED:
                print(mail.retry_after)
                print()

            data.append(mail)

    unprocessed_mails = await read_unprocessed_mails_usecase(read_all_mails_dto)

    assert count == len(unprocessed_mails)
    assert sorted(unprocessed_mails, key=lambda x: x.id) == sorted(
        data, key=lambda x: x.id
    )
