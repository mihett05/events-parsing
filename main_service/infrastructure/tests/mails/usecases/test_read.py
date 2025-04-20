import random

import pytest

from application.mails.usecases import ReadMailUseCase
from domain.mails.entities import Mail
from domain.mails.exceptions import MailNotFound


@pytest.mark.asyncio
async def test_read_success(
    read_mail_usecase: ReadMailUseCase,
    create_mail: Mail,
):
    mail = await read_mail_usecase(create_mail.id)
    assert mail == create_mail


@pytest.mark.asyncio
async def test_read_not_found(read_mail_usecase: ReadMailUseCase):
    with pytest.raises(MailNotFound):
        await read_mail_usecase(random.randint(100, 200))
