import asyncio
from datetime import datetime

import pytest
from domain.events.entities import Event
from domain.mails.dtos import ParsedMailInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User

from infrastructure.config import Config
from infrastructure.gateways.mails.gateway import ImapEmailsGateway
from infrastructure.gateways.notifications.gateways.mail import (
    NotificationEmailGateway,
)


@pytest.mark.asyncio
async def test_parse_mails_attachments(
    imap_email_gateway: ImapEmailsGateway,
    create_mails: list[ParsedMailInfoDto],
    notification_email_gateway: NotificationEmailGateway,
    get_config: Config,
    get_user_entity: User,
):
    now = datetime.now()
    event = Event(title="Example", start_date=now, location=None, id=-1)
    for mail in create_mails:
        await notification_email_gateway.send(
            notification=Notification(
                text=mail.raw_content.decode("utf-8"),
                recipient_id=get_user_entity.id,
                event_id=event.id,
                send_date=now.date(),
            ),
            recipient=get_user_entity,
            attachments=mail.attachments,
        )
    await asyncio.sleep(0.1)
    mails = await imap_email_gateway.receive_mails()
    attrs = ("theme", "sender", "raw_content", "received_date", "attachments")
    mails.sort(key=lambda x: x.imap_mail_uid)
    for attr in attrs:
        for i in range(len(create_mails)):
            if attr == "attachments":
                for j in range(len(getattr(create_mails[i], attr))):
                    assert (
                        getattr(mails[i], attr)[j].filename
                        == getattr(create_mails[i], attr)[j].filename
                    )
                    assert (
                        getattr(mails[i], attr)[j].extension
                        == getattr(create_mails[i], attr)[j].extension
                    )
                    assert (
                        getattr(mails[i], attr)[j].content.getvalue()
                        == getattr(create_mails[i], attr)[j].content.getvalue()
                    )
            else:
                assert getattr(mails[i], attr) == getattr(create_mails[i], attr)
