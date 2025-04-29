import pytest
from application.mails.usecases import CreateMailUseCase
from domain.mails.dtos import CreateMailDto


@pytest.mark.asyncio
async def test_create_success(
    create_mail_usecase: CreateMailUseCase,
    create_mail_dto: CreateMailDto,
):
    mail = await create_mail_usecase(dto=create_mail_dto)

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
