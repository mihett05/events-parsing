import asyncio

from domain.attachments.dtos import ParsedAttachmentInfoDto
from domain.notifications.entities import Notification
from domain.users.entities import User

from infrastructure.gateways.notifications.gateways import (
    NotificationEmailGateway,
)


class NotificationEmailMemoryGateway(NotificationEmailGateway):
    def __init__(self):
        super().__init__(
            smtp_server="avtobot",
            smtp_port=123,
            imap_username="misha",
            imap_password="spit po 25 chasov v den'",
        )

    async def __aenter__(self):
        print("entering notification email gateway context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("exiting notification email gateway context")

    async def send(
        self,
        notification: Notification,
        recipient: User,
        attachments: list[ParsedAttachmentInfoDto] = None,
    ):
        await asyncio.sleep(0.1)  # imitation of publishing mails to process
