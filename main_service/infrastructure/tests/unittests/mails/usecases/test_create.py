import pytest
from application.mails.usecases import CreateMailsUseCase
from domain.mails.dtos import CreateMailDto


@pytest.mark.asyncio
async def test_create_success(
    create_mails_usecase: CreateMailsUseCase,
    create_mail_dto: CreateMailDto,
):
    mails, _ = await create_mails_usecase(dtos=[create_mail_dto], actor=None)
    mail = mails[0]

    attrs = (
        "theme",
        "sender",
        "raw_content",
        "received_date",
        "state",
        "retry_after",
    )
    for attr in attrs:
        assert getattr(mail, attr) == getattr(create_mail_dto, attr)

    assert mail.id == 1
