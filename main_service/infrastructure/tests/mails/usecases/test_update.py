from copy import copy

import pytest

from application.mails.dtos import UpdateMailDto
from application.mails.usecases import UpdateMailUseCase
from domain.mails.entities import Mail
from domain.mails.exceptions import MailNotFound


@pytest.mark.asyncio
async def test_update_success(
    update_mail_usecase: UpdateMailUseCase,
    update_mail_dto: UpdateMailDto,
    create_mail: Mail,
):
    create_mail = copy(create_mail)
    mail = await update_mail_usecase(update_mail_dto)

    assert mail.state != create_mail.state
    assert mail.state == update_mail_dto.state


@pytest.mark.asyncio
async def test_update_not_found(
    update_mail_usecase: UpdateMailUseCase,
    update_mail_dto: UpdateMailDto,
):
    update_mail_dto.mail_id = 42
    with pytest.raises(MailNotFound):
        _ = await update_mail_usecase(update_mail_dto)
