import pytest
from domain.mails.dtos import ParsedMailInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User

from infrastructure.gateways.mails.gateway import ImapEmailsGateway
from infrastructure.gateways.notifications.gateways.mail import (
    NotificationEmailGateway,
)


@pytest.mark.asyncio
async def test_parse_mails_attachments(
    imap_gateway: ImapEmailsGateway,
    parsed_mails: list[ParsedMailInfoDto],
    mail_gateway: NotificationEmailGateway,
):
    for mail in parsed_mails:
        await mail_gateway.send(
            notification=Notification(text="Тестовое сообщение"),
            recipient=User(email="events-parsing@mail.ru", fullname="Nick"),
            attachments=mail.attachments,
        )
    mails = await imap_gateway.receive_mails()
    attrs = ("theme", "sender", "raw_content", "received_date", "attachments")
    mails.sort(key=lambda x: x.imap_mail_uid)
    for attr in attrs:
        for i in range(len(mails)):
            assert getattr(mails[i], attr) == getattr(parsed_mails[i], attr)
